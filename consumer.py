#!/usr/bin/env python3
# thoth-investigator-consumer
# Copyright(C) 2020 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Consume messages to schedule workflows to learn something about a package."""


import logging
import os
from time import time
from datetime import timedelta

from thoth.messaging import MessageBase

from thoth.messaging import AdviseJustificationMessage
from thoth.messaging import AdviserReRunMessage
from thoth.messaging import AdviserTriggerMessage
from thoth.messaging import HashMismatchMessage
from thoth.messaging import KebechetTriggerMessage
from thoth.messaging import MissingPackageMessage
from thoth.messaging import MissingVersionMessage
from thoth.messaging import PackageExtractTriggerMessage
from thoth.messaging import PackageReleasedMessage
from thoth.messaging import ProvenanceCheckerTriggerMessage
from thoth.messaging import QebHwtTriggerMessage
from thoth.messaging import SIUnanalyzedPackageMessage
from thoth.messaging import SolvedPackageMessage
from thoth.messaging import UnresolvedPackageMessage
from thoth.messaging import UnrevsolvedPackageMessage


from investigator.investigator import __service_version__
from investigator.investigator.advise_justification import expose_advise_justification_metrics
from investigator.investigator.adviser_re_run import parse_adviser_re_run_message
from investigator.investigator.adviser_trigger import parse_adviser_trigger_message
from investigator.investigator.hash_mismatch import parse_hash_mismatch
from investigator.investigator.kebechet_trigger import parse_kebechet_trigger_message
from investigator.investigator.missing_package import parse_missing_package
from investigator.investigator.missing_version import parse_missing_version
from investigator.investigator.package_extract_trigger import parse_package_extract_trigger_message
from investigator.investigator.package_released import parse_package_released_message
from investigator.investigator.provenance_checker_trigger import parse_provenance_checker_trigger_message
from investigator.investigator.qebhwt_trigger import parse_qebhwt_trigger_message
from investigator.investigator.si_unanalyzed_package import parse_si_unanalyzed_package_message
from investigator.investigator.solved_package import parse_solved_package_message
from investigator.investigator.unrevsolved_package import parse_revsolved_package_message
from investigator.investigator.unresolved_package import parse_unresolved_package_message

from thoth.common import OpenShift, init_logging
from thoth.storages.graph import GraphDatabase

from aiohttp import web
from prometheus_client import generate_latest

from faust import Topic
from faust.types.tuples import TP

# set up logging
DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth Investigator consumer v%s", __service_version__)

# initialize the application
app = MessageBase().app

# Get all topics
advise_justification_message_topic = AdviseJustificationMessage().topic
adviser_re_run_message_topic = AdviserReRunMessage().topic
adviser_trigger_message_topic = AdviserTriggerMessage().topic
hash_mismatch_message_topic = HashMismatchMessage().topic
kebechet_trigger_message_topic = KebechetTriggerMessage().topic
missing_package_message_topic = MissingPackageMessage().topic
missing_version_message_topic = MissingVersionMessage().topic
package_extract_trigger_message_topic = PackageExtractTriggerMessage().topic
package_released_message_topic = PackageReleasedMessage().topic
provenance_checker_trigger_message_topic = ProvenanceCheckerTriggerMessage().topic
qebhwt_trigger_message_topic = QebHwtTriggerMessage().topic
solved_package_message_topic = SolvedPackageMessage().topic
unresolved_package_message_topic = UnresolvedPackageMessage().topic
unrevsolved_package_message_topic = UnrevsolvedPackageMessage().topic
si_unanalyzed_package_message_topic = SIUnanalyzedPackageMessage().topic

openshift = OpenShift()
graph = GraphDatabase()

graph.connect()

window_size = float(os.getenv("THOTH_INVESTIGATOR_TABLE_WINDOW", 1))
window_expiration = float(os.getenv("THOTH_INVESTIGATOR_WINDOW_EXPIRATION", 12))
# we should allow the time deltas to be passed as params (TEMPORARY)
offset_table = (
    app.Table("partition_offsets", default=int)
    .tumbling(timedelta(minutes=window_size), timedelta(hours=window_expiration))
    .relative_to_now()
)


@app.task()
async def after_initialization():
    """Run things after the app has started."""
    init_logging()


@app.page("/metrics")
async def get_metrics(self, request):
    """Serve the metrics from the consumer registry."""
    return web.Response(text=generate_latest().decode("utf-8"))


@app.page("/_health")
async def get_health(self, request):
    """Serve a readiness/liveness probe endpoint."""
    data = {"status": "ready", "version": __service_version__}
    return web.json_response(data)


@app.page("/seek/{topic_name}")
async def seek_offset(self, request, topic_name):
    """Set offsets for a specific topic based of a time stamp."""
    # timestamp should be passed in seconds since utc epoch
    utc_timestamp = float(request.query["timestamp"])
    topic = globals()[topic_name]
    if not type(topic) == Topic:
        raise TypeError("The passed topic is not known.")

    # Get time delta from timestamp
    delta_seconds = time() - utc_timestamp

    # both of these errors should
    if delta_seconds < 0:
        raise ValueError("The timestamp given is from the future, I am not a fortune teller.")
    elif timedelta(seconds=delta_seconds) > timedelta(hours=6):
        raise Exception("Given time is beyond expiration limit.")

    for p in topic.partitions:
        # the application has a global consumer which directs and manages the streams/topics and more importantly
        # maintains the offsets for our streams
        await app.consumer.seek(
            TP(topic=topic.get_topic_name(), partition=p), offset_table[(topic, p)].delta(delta_seconds),
        )

    return web.json_response({"status": "success"})


@app.agent(advise_justification_message_topic)
async def consume_advise_justification(stream):
    """Loop when an advise justification message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(advise_justification_message_topic, partition)] = offset

        expose_advise_justification_metrics(advise_justification=message.value)


@app.agent(adviser_re_run_message_topic)
async def consume_adviser_re_run(stream):
    """Loop when an adviser re run message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(adviser_re_run_message_topic, partition)] = offset

        parse_adviser_re_run_message(adviser_re_run=message.value, openshift=openshift)


@app.agent(adviser_trigger_message_topic)
async def consume_adviser_trigger(stream):
    """Loop when an adviser trigger message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(adviser_trigger_message_topic, partition)] = offset

        parse_adviser_trigger_message(adviser_trigger=message.value, openshift=openshift)


@app.agent(hash_mismatch_message_topic)
async def consume_hash_mismatch(stream):
    """Loop when an hash mismatch message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(hash_mismatch_message_topic, partition)] = offset

        parse_hash_mismatch(mismatch=message.value, openshift=openshift, graph=graph)


@app.agent(kebechet_trigger_message_topic)
async def consume_kebechet_trigger(stream):
    """Loop when a kebechet_trigger message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(kebechet_trigger_message_topic, partition)] = offset

        parse_kebechet_trigger_message(kebechet_trigger=message.value, openshift=openshift)


@app.agent(missing_package_message_topic)
async def consume_missing_package(stream):
    """Loop when an missing package message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(missing_package_message_topic, partition)] = offset

        parse_missing_package(package=message.value, openshift=openshift, graph=graph)


@app.agent(missing_version_message_topic)
async def consume_missing_version(stream):
    """Loop when an missing version message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(missing_version_message_topic, partition)] = offset

        parse_missing_version(version=message.value, openshift=openshift, graph=graph)


@app.agent(package_extract_trigger_message_topic)
async def consume_package_extract_trigger(stream):
    """Loop when a package_extract_trigger message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(package_extract_trigger_message_topic, partition)] = offset

        parse_package_extract_trigger_message(package_extract_trigger=message.value, openshift=openshift)


@app.agent(package_released_message_topic)
async def consume_package_released(stream) -> None:
    """Loop when a package released message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(package_released_message_topic, partition)] = offset

        parse_package_released_message(package_released=message.value, openshift=openshift, graph=graph)


@app.agent(provenance_checker_trigger_message_topic)
async def consume_provenance_checker_trigger(stream):
    """Loop when a provenance_checker_trigger message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(provenance_checker_trigger_message_topic, partition)] = offset

        parse_provenance_checker_trigger_message(
            provenance_checker_trigger=message.value, openshift=openshift,
        )


@app.agent(qebhwt_trigger_message_topic)
async def consume_qebhwt_trigger(stream):
    """Loop when a qebhwt_trigger message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(qebhwt_trigger_message_topic, partition)] = offset

        parse_qebhwt_trigger_message(qebhwt_trigger=message.value, openshift=openshift)


@app.agent(si_unanalyzed_package_message_topic)
async def consume_si_unanalyzed_package(stream) -> None:
    """Loop when an SI Unanalyzed package message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(si_unanalyzed_package_message_topic, partition)] = offset

        parse_si_unanalyzed_package_message(si_unanalyzed_package=message.value, openshift=openshift, graph=graph)


@app.agent(solved_package_message_topic)
async def consume_solved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(solved_package_message_topic, partition)] = offset

        parse_solved_package_message(solved_package=message.value, openshift=openshift, graph=graph)


@app.agent(unresolved_package_message_topic)
async def consume_unresolved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(unresolved_package_message_topic, partition)] = offset

        parse_unresolved_package_message(unresolved_package=message.value, openshift=openshift, graph=graph)


@app.agent(unrevsolved_package_message_topic)
async def consume_unrevsolved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for event in stream.events():
        message = event.message
        partition = message.partition
        offset = message.offset
        offset_table[(unrevsolved_package_message_topic, partition)] = offset

        parse_revsolved_package_message(unrevsolved_package=message.value, openshift=openshift)


if __name__ == "__main__":
    app.main()
