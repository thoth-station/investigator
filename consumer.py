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
from thoth.messaging import HashMismatchMessage
from thoth.messaging import MissingPackageMessage
from thoth.messaging import MissingVersionMessage
from thoth.messaging import SolvedPackageMessage
from thoth.messaging import UnresolvedPackageMessage
from thoth.messaging import UnrevsolvedPackageMessage


from investigator.investigator import __service_version__
from investigator.investigator.advise_justification import expose_advise_justification_metrics
from investigator.investigator.adviser_re_run import parse_adviser_re_run_message
from investigator.investigator.hash_mismatch import parse_hash_mismatch
from investigator.investigator.missing_package import parse_missing_package
from investigator.investigator.missing_version import parse_missing_version
from investigator.investigator.solved_package import parse_solved_package_message
from investigator.investigator.unrevsolved_package import parse_revsolved_package_message
from investigator.investigator.unresolved_package import parse_unresolved_package_message


from thoth.common import OpenShift, init_logging
from thoth.storages.graph import GraphDatabase

from aiohttp import web
from prometheus_client import generate_latest

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
hash_mismatch_message_topic = HashMismatchMessage().topic
missing_package_message_topic = MissingPackageMessage().topic
missing_version_message_topic = MissingVersionMessage().topic
solved_package_message_topic = SolvedPackageMessage().topic
unresolved_package_message_topic = UnresolvedPackageMessage().topic
unrevsolved_package_message_topic = UnrevsolvedPackageMessage().topic

openshift = OpenShift()
graph = GraphDatabase()

graph.connect()


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


@app.agent(advise_justification_message_topic)
async def consume_advise_justification(advise_justifications):
    """Loop when an advise justification message is received."""
    async for advise_justification in advise_justifications:
        expose_advise_justification_metrics(advise_justification=advise_justification)


@app.agent(adviser_re_run_message_topic)
async def consume_adviser_re_run(adviser_re_runs):
    """Loop when an adviser re run message is received."""
    async for adviser_re_run in adviser_re_runs:
        parse_adviser_re_run_message(adviser_re_run=adviser_re_run, openshift=openshift)


@app.agent(hash_mismatch_message_topic)
async def consume_hash_mismatch(hash_mismatches):
    """Loop when an hash mismatch message is received."""
    async for hash_mismatch in hash_mismatches:
        parse_hash_mismatch(mismatch=hash_mismatch, openshift=openshift, graph=graph)


@app.agent(missing_package_message_topic)
async def consume_missing_package(missing_packages):
    """Loop when an missing package message is received."""
    async for missing_package in missing_packages:
        parse_missing_package(package=missing_package, openshift=openshift, graph=graph)


@app.agent(missing_version_message_topic)
async def consume_missing_version(missing_versions):
    """Loop when an missing version message is received."""
    async for missing_version in missing_versions:
        parse_missing_version(version=missing_version, openshift=openshift, graph=graph)


@app.agent(solved_package_message_topic)
async def consume_solved_package(solved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for solved_package in solved_packages:
        parse_solved_package_message(solved_package=solved_package, openshift=openshift, graph=graph)


@app.agent(unresolved_package_message_topic)
async def consume_unresolved_package(unresolved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for unresolved_package in unresolved_packages:
        parse_unresolved_package_message(unresolved_package=unresolved_package, openshift=openshift, graph=graph)


@app.agent(unrevsolved_package_message_topic)
async def consume_unrevsolved_package(unrevsolved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for unrevsolved_package in unrevsolved_packages:
        parse_revsolved_package_message(unrevsolved_package=unrevsolved_package, openshift=openshift)


if __name__ == "__main__":
    app.main()
