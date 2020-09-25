#!/usr/bin/env python3
# thoth-investigator-producer
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

"""Produces messages regarding package depending on the component in which is used."""

import logging
import os

from investigator.investigator import __service_version__
from thoth.messaging import MessageBase
from thoth.messaging.unresolved_package import UnresolvedPackageMessage
from investigator.investigator.unresolved_package import investigate_unresolved_package

import asyncio

app = MessageBase().app

DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth Investigator producer v%s", __service_version__)

_COMPONENT_NAME = "thoth-investigator"


@app.command()
async def main() -> None:
    """Produce Kafka messages for unresolved package identified."""
    unresolved_package = UnresolvedPackageMessage()
    unresolved_packages, solver = investigate_unresolved_package()
    async_tasks = []
    for package in unresolved_packages:
        package_name = unresolved_packages[package].name
        package_version = unresolved_packages[package].version

        sources = []
        if unresolved_packages[package].index:
            sources = [unresolved_packages[package].index]

        try:
            async_tasks.append(
                unresolved_package.publish_to_topic(
                    unresolved_package.MessageContents(
                        package_name=package_name,
                        package_version=package_version,
                        index_url=sources,
                        solver=solver,
                        service_version=__service_version__,
                        component_name=_COMPONENT_NAME,
                    )
                )
            )
            _LOGGER.info(
                "Unresolved package (package name:%r, package version:%r, index_url:%r, solver:%r)",
                package_name,
                package_version,
                sources,
                solver,
            )

        except Exception as identifier:
            _LOGGER.exception("Failed to publish with the following error message: %r", identifier)

    await asyncio.gather(*async_tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
