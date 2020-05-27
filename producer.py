#!/usr/bin/env python3
# thoth-unresolved-package-handler
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

"""This is run to send messages regarding unresolved packages that need to be solved with priority."""

import logging
import os

from thoth.messaging import MessageBase
from thoth.messaging.unresolved_package import UnresolvedPackageMessage
from thoth.unresolved_package_handler.unresolved_package_handler import unresolved_package_handler

app = MessageBase.app

DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger("thoth.unresolved_package_handler")


@app.command()
async def main() -> None:
    """Run advise-reporter."""
    unresolved_package = UnresolvedPackageMessage()
    unresolved_packages, solver = unresolved_package_handler()

    for package in unresolved_packages:
        package_name = unresolved_packages[package].name
        package_version = unresolved_packages[package].version
        sources = [unresolved_packages[package].index]

        try:
            await unresolved_package.publish_to_topic(
                unresolved_package.MessageContents(
                    package_name=package_name, package_version=package_version, index_url=sources, solver=solver
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


if __name__ == "__main__":
    app.main()
