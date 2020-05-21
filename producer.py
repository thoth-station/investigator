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

import asyncio
import logging

from thoth.messaging import MessageBase
from thoth.messaging.unresolved_package import UnresolvedPackageMessage
from unresolved_package_handler import unresolved_package_handler

app = MessageBase.app

_LOGGER = logging.getLogger("thoth.unresolved_package_handler")


@app.command()
async def main():
    """Run advise-reporter."""
    unresolved_package = UnresolvedPackageMessage()
    unresolved_packages, package_version, sources, solver = unresolved_package_handler()

    for package_name in unresolved_packages:
        try:
            await unresolved_package.publish_to_topic(
                unresolved_package.MessageContents(
                    package_name=package_name, package_version=package_version, index_url=sources, solver=solver
                )
            )
            _LOGGER.info(
                "Unresolved package (package name:%r, package version:%r, index_url:%r, runtime_environment:%r)",
                package_name,
                package_version,
                sources,
                runtime_environment,
            )

        except Exception as identifier:
            _LOGGER.exception("Failed to publish with the following error message: %r", identifier)


if __name__ == "__main__":
    app.main()
