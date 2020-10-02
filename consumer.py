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
from thoth.messaging import UpdateProvidesSourceDistroMessage


from investigator.investigator import __service_version__
from investigator.investigator.configuration import Configuration
import investigator.investigator.advise_justification as advise_justification
import investigator.investigator.adviser_re_run as adviser_re_run
import investigator.investigator.adviser_trigger as adviser_trigger
import investigator.investigator.hash_mismatch as hash_mismatch
import investigator.investigator.kebechet_trigger as kebechet_trigger
import investigator.investigator.missing_package as missing_package
import investigator.investigator.missing_version as missing_version
import investigator.investigator.package_extract_trigger as package_extract_trigger
import investigator.investigator.package_released as package_released
import investigator.investigator.provenance_checker_trigger as provenance_checker_trigger
import investigator.investigator.qebhwt_trigger as qebhwt_trigger
import investigator.investigator.si_unanalyzed_package as si_unanalyzed_package
import investigator.investigator.solved_package as solved_package
import investigator.investigator.unrevsolved_package as unrevsolved_package
import investigator.investigator.unresolved_package as unresolved_package
import investigator.investigator.update_provide_source_distro as update_provide_source_distro

from thoth.common import OpenShift, init_logging
from thoth.storages.graph import GraphDatabase

from aiohttp import web
from prometheus_client import generate_latest

# initialize the application
app = MessageBase().app

init_logging()

# set up logging
DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth Investigator consumer v%s", __service_version__)

# Conditional scheduling, by default we schedule everything.
_LOGGER.info("Schedule Solver Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER)
_LOGGER.info("Schedule Reverse Solver Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER)
_LOGGER.info("Schedule Unanalyzed SI Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY)

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
si_unanalyzed_package_message_topic = SIUnanalyzedPackageMessage().topic
solved_package_message_topic = SolvedPackageMessage().topic
unresolved_package_message_topic = UnresolvedPackageMessage().topic
unrevsolved_package_message_topic = UnrevsolvedPackageMessage().topic
update_provide_source_distro_message_topic = UpdateProvidesSourceDistroMessage().topic


openshift = OpenShift()
graph = GraphDatabase()

graph.connect()


@app.page("/metrics")
async def get_metrics(self, request):
    """Serve the metrics from the consumer registry."""
    return web.Response(text=generate_latest().decode("utf-8"))


@app.page("/_health")
async def get_health(self, request):
    """Serve a readiness/liveness probe endpoint."""
    data = {"status": "ready", "version": __service_version__}
    return web.json_response(data)


@app.agent(advise_justification_message_topic)
async def consume_advise_justification(stream):
    """Loop when an advise justification message is received."""
    async for message in stream:
        await advise_justification.handler_table[message.version](advise_justification=message)


@app.agent(adviser_re_run_message_topic)
async def consume_adviser_re_run(stream):
    """Loop when an adviser re run message is received."""
    async for message in stream:
        await adviser_re_run.handler_table[message.version](adviser_re_run=message, openshift=openshift)


@app.agent(adviser_trigger_message_topic)
async def consume_adviser_trigger(stream):
    """Loop when an adviser trigger message is received."""
    async for message in stream:
        await adviser_trigger.handler_table[message.version](adviser_trigger=message, openshift=openshift)


@app.agent(hash_mismatch_message_topic)
async def consume_hash_mismatch(stream):
    """Loop when an hash mismatch message is received."""
    async for message in stream:
        await hash_mismatch.handler_table[message.version](mismatch=message, openshift=openshift, graph=graph)


@app.agent(update_provide_source_distro_message_topic)
async def consume_update_provide_source_distro(stream):
    """Loop when update_provide_source_distro message is received."""
    async for message in stream:
        await update_provide_source_distro.handler_table[message.version](
            update_provide_source_distro=message, graph=graph
        )


@app.agent(kebechet_trigger_message_topic)
async def consume_kebechet_trigger(stream):
    """Loop when a kebechet_trigger message is received."""
    async for message in stream:
        await kebechet_trigger.handler_table[message.version](kebechet_trigger=message, openshift=openshift)


@app.agent(missing_package_message_topic)
async def consume_missing_package(stream):
    """Loop when an missing package message is received."""
    async for message in stream:
        await missing_package.handler_table[message.version](package=message, openshift=openshift, graph=graph)


@app.agent(missing_version_message_topic)
async def consume_missing_version(stream):
    """Loop when an missing version message is received."""
    async for message in stream:
        await missing_version.handler_table[message.version](version=message, openshift=openshift, graph=graph)


@app.agent(package_extract_trigger_message_topic)
async def consume_package_extract_trigger(stream):
    """Loop when a package_extract_trigger message is received."""
    async for message in stream:
        await package_extract_trigger.handler_table[message.version](
            package_extract_trigger=message, openshift=openshift,
        )


@app.agent(package_released_message_topic)
async def consume_package_released(stream) -> None:
    """Loop when a package released message is received."""
    async for message in stream:
        await package_released.handler_table[message.version](
            package_released=message, openshift=openshift, graph=graph,
        )


@app.agent(provenance_checker_trigger_message_topic)
async def consume_provenance_checker_trigger(stream):
    """Loop when a provenance_checker_trigger message is received."""
    async for message in stream:
        await provenance_checker_trigger.handler_table[message.version](
            provenance_checker_trigger=message, openshift=openshift
        )


@app.agent(qebhwt_trigger_message_topic)
async def consume_qebhwt_trigger(stream):
    """Loop when a qebhwt_trigger message is received."""
    async for message in stream:
        await qebhwt_trigger.handler_table[message.version](
            qebhwt_trigger=message, openshift=openshift,
        )


@app.agent(si_unanalyzed_package_message_topic)
async def consume_si_unanalyzed_package(stream) -> None:
    """Loop when an SI Unanalyzed package message is received."""
    async for message in stream:
        await si_unanalyzed_package.handler_table[message.version](
            si_unanalyzed_package=message, openshift=openshift, graph=graph,
        )


@app.agent(solved_package_message_topic)
async def consume_solved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for message in stream:
        await solved_package.handler_table[message.version](solved_package=message, openshift=openshift, graph=graph)


@app.agent(unresolved_package_message_topic)
async def consume_unresolved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for message in stream:
        await unresolved_package.handler_table[message.version](
            unresolved_package=message, openshift=openshift, graph=graph
        )


@app.agent(unrevsolved_package_message_topic)
async def consume_unrevsolved_package(stream) -> None:
    """Loop when an unresolved package message is received."""
    async for message in stream:
        await unrevsolved_package.handler_table[message.version](unrevsolved_package=message, openshift=openshift)


if __name__ == "__main__":
    app.main()
