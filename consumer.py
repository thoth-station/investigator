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


from investigator.investigator import __service_version__
from investigator.investigator.configuration import Configuration
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
_LOGGER.info(
    "Schedule Reverse Solver Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER
)
_LOGGER.info(
    "Schedule Unanalyzed SI Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY
)

# Get all topics
advise_justification_message_topic = AdviseJustificationMessage().topic
adviser_re_run_message_topic = AdviserReRunMessage().topic
adviser_trigger_message_topic = AdviserTriggerMessage().topic
hash_mismatch_message_topic = HashMismatchMessage().topic
kebechet_trigger_message_topic = KebechetTriggerMessage().topic
missing_package_message_topic = MissingPackageMessage().topic
missing_version_message_topic = MissingVersionMessage().topic
package_extract_trigger_message_topic = PackageExtractTriggerMessage().topic
provenance_checker_trigger_message_topic = ProvenanceCheckerTriggerMessage().topic
qebhwt_trigger_message_topic = QebHwtTriggerMessage().topic
solved_package_message_topic = SolvedPackageMessage().topic
unresolved_package_message_topic = UnresolvedPackageMessage().topic
unrevsolved_package_message_topic = UnrevsolvedPackageMessage().topic
si_unanalyzed_package_message_topic = SIUnanalyzedPackageMessage().topic

package_released_message_topic = PackageReleasedMessage().topic

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
async def consume_advise_justification(advise_justifications):
    """Loop when an advise justification message is received."""
    async for advise_justification in advise_justifications:
        await expose_advise_justification_metrics(advise_justification=advise_justification)


@app.agent(adviser_re_run_message_topic)
async def consume_adviser_re_run(adviser_re_runs):
    """Loop when an adviser re run message is received."""
    async for adviser_re_run in adviser_re_runs:
        await parse_adviser_re_run_message(adviser_re_run=adviser_re_run, openshift=openshift)


@app.agent(adviser_trigger_message_topic)
async def consume_adviser_trigger(adviser_triggers):
    """Loop when an adviser trigger message is received."""
    async for adviser_trigger in adviser_triggers:
        await parse_adviser_trigger_message(adviser_trigger=adviser_trigger, openshift=openshift)


@app.agent(hash_mismatch_message_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Loop when an hash mismatch message is received."""
    async for hash_mismatch in hash_mismatches:
        await parse_hash_mismatch(mismatch=hash_mismatch, openshift=openshift, graph=graph)


@app.agent(kebechet_trigger_message_topic)
async def consume_kebechet_trigger(kebechet_triggers):
    """Loop when a kebechet_trigger message is received."""
    async for kebechet_trigger in kebechet_triggers:
        await parse_kebechet_trigger_message(kebechet_trigger=kebechet_trigger, openshift=openshift)


@app.agent(missing_package_message_topic)
async def consume_missing_package(missing_packages):
    """Loop when an missing package message is received."""
    async for missing_package in missing_packages:
        await parse_missing_package(package=missing_package, openshift=openshift, graph=graph)


@app.agent(missing_version_message_topic)
async def consume_missing_version(missing_versions):
    """Loop when an missing version message is received."""
    async for missing_version in missing_versions:
        await parse_missing_version(version=missing_version, openshift=openshift, graph=graph)


@app.agent(package_extract_trigger_message_topic)
async def consume_package_extract_trigger(package_extract_triggers):
    """Loop when a package_extract_trigger message is received."""
    async for package_extract_trigger in package_extract_triggers:
        await parse_package_extract_trigger_message(
            package_extract_trigger=package_extract_trigger, openshift=openshift
        )


@app.agent(package_released_message_topic)
async def consume_package_released(package_releases) -> None:
    """Loop when a package released message is received."""
    async for package_released in package_releases:
        await parse_package_released_message(package_released=package_released, openshift=openshift, graph=graph)


@app.agent(provenance_checker_trigger_message_topic)
async def consume_provenance_checker_trigger(provenance_checker_triggers):
    """Loop when a provenance_checker_trigger message is received."""
    async for provenance_checker_trigger in provenance_checker_triggers:
        await parse_provenance_checker_trigger_message(
            provenance_checker_trigger=provenance_checker_trigger, openshift=openshift,
        )


@app.agent(qebhwt_trigger_message_topic)
async def consume_qebhwt_trigger(qebhwt_triggers):
    """Loop when a qebhwt_trigger message is received."""
    async for qebhwt_trigger in qebhwt_triggers:
        await parse_qebhwt_trigger_message(qebhwt_trigger=qebhwt_trigger, openshift=openshift)


@app.agent(si_unanalyzed_package_message_topic)
async def consume_si_unanalyzed_package(si_unanalyzed_packages) -> None:
    """Loop when an SI Unanalyzed package message is received."""
    async for si_unanalyzed_package in si_unanalyzed_packages:
        await parse_si_unanalyzed_package_message(
            si_unanalyzed_package=si_unanalyzed_package, openshift=openshift, graph=graph
        )


@app.agent(solved_package_message_topic)
async def consume_solved_package(solved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for solved_package in solved_packages:
        await parse_solved_package_message(solved_package=solved_package, openshift=openshift, graph=graph)


@app.agent(unresolved_package_message_topic)
async def consume_unresolved_package(unresolved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for unresolved_package in unresolved_packages:
        await parse_unresolved_package_message(unresolved_package=unresolved_package, openshift=openshift, graph=graph)


@app.agent(unrevsolved_package_message_topic)
async def consume_unrevsolved_package(unrevsolved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for unrevsolved_package in unrevsolved_packages:
        await parse_revsolved_package_message(unrevsolved_package=unrevsolved_package, openshift=openshift)


if __name__ == "__main__":
    app.main()
