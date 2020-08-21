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

from thoth.investigator import __service_version__

from thoth.messaging import MessageBase
from thoth.messaging import UnresolvedPackageMessage
from thoth.messaging import UnrevsolvedPackageMessage
from thoth.messaging import SolvedPackageMessage
from thoth.investigator.investigate_unresolved_package import parse_unresolved_package_message
from thoth.investigator.investigate_solved_package import parse_solved_package_message
from thoth.investigator.investigate_unrevsolved_package import parse_revsolved_package_message

from thoth.common import OpenShift
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
unresolved_package_message_topic = UnresolvedPackageMessage().topic
unrevsolved_package_message_topic = UnrevsolvedPackageMessage().topic
solved_package_message_topic = SolvedPackageMessage().topic

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


@app.agent(solved_package_message_topic)
async def consume_solved_package(solved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for solved_package in solved_packages:
        parse_solved_package_message(solved_package=solved_package, openshift=openshift, graph=graph)


if __name__ == "__main__":
    app.main()
