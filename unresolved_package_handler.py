#!/usr/bin/env python3
# thoth-storages
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

"""This is run to send messages regarding unsolved packages that need to be solved with priorities."""

import asyncio
import logging
import faust
import os
import ssl
import json
import sys

from thoth.messaging import UnresolvedPackageMessage

app = MessageBase.app

_LOGGER = logging.getLogger("thoth.unresolved_package_handler")


@app.command()
async def main():
    """Run advise-reporter."""
    adviser_run_path = os.environ["FILE_PATH"]
    sources_json_path = "result.parameters.project.requirements.source"

    with open(adviser_run_path, "r") as f:
        content = json.load(f)

    unresolved_packages = []
    report = content["result"]["report"]
    if report:
        errors_details = report.get("_ERROR_DETAILS")
        if errors_details:
            unresolved_packages = errors_details["unresolved"]

    if not unresolved_packages:
        _LOGGER.warning("No packages to be solved with priority")
        sys.exit(2)

    sources = []
    parameters = content["result"]["parameters"]
    requirements = parameters["project"].get("requirements")
    if requirements:
        sources = [source["url"] for source in requirements["source"]]

    runtime_environment = parameters["project"].get("runtime_environment")

    solver = None
    operating_system = runtime_environment.get("operating_system", {})
    if operating_system:
        os_name = runtime_environment["operating_system"].get("name")
        os_version=_normalize_os_version(operating_system.get("name"), operating_system.get("version"))
        python_version = runtime_environment.get("python_version")
        solver = "solver" + "-" + os_name + "-" + os_version + "-" + "py" + "".join(runtime_environment["python_version"].split("."))

    for unresolved_package in unresolved_packages:
        if sources:
            for index_url in sources:
                try:
                    await unresolved_package.publish_to_topic(
                        unresolved_package.MessageContents(
                            package_name=package_name,
                            package_version=package_version,
                            index_url=index_url,
                            solver=solver,
                        )
                    )
                    _LOGGER.debug(
                        "Unresolved package:\npackage name:%r\npackage version:%r\nindex_url:%r\nruntime_environment:%r\n",
                        package_name,
                        package_version,
                        index_url,
                        runtime_environment,
                    )

                except Exception as identifier:
                    _LOGGER.exception("Failed to publish with the following error message: %r", identifier)


if __name__ == "__main__":
    app.main()
