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
import json
import os

from typing import Optional
from pathlib import Path

from thoth.storages.graph import GraphDatabase

_LOGGER = logging.getLogger("thoth.unresolved_package_handler")


def unresolved_package_handler(file_test_path: Optional[Path] = None):
    """Run Unresolved Package Handler"""
    if file_test_path:
        _LOGGER.debug("Dry run..")
        adviser_run_path = file_test_path
    else:
        adviser_run_path = os.environ["FILE_PATH"]

    sources_json_path = "result.parameters.project.requirements.source"

    if not Path(adviser_run_path).exists():
        raise FileNotFoundError(f"Cannot find the file on this path: {adviser_run_path}")

    with open(adviser_run_path, "r") as f:
        content = json.load(f)

    unresolved_packages = []
    report = content["result"]["report"]
    if report:
        errors_details = report.get("_ERROR_DETAILS")
        if errors_details:
            unresolved_packages = errors_details["unresolved"]

    if not unresolved_packages:
        _LOGGER.warning("No packages to be solved with priority identified.")
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
        os_version=GraphDatabase().normalize_os_version(operating_system.get("name"), operating_system.get("version"))
        python_version = runtime_environment.get("python_version")
        solver = "solver" + "-" + os_name + "-" + os_version + "-" + "py" + "".join(runtime_environment["python_version"].split("."))

        GraphDatabase().parse_python_solver_name(solver)

    package_version  = None

    _LOGGER.info(f"Unresolved packages identified.. {unresolved_packages}")
    _LOGGER.info(f"package versions identified.. {package_version}")
    _LOGGER.info(f"Sources identified.. {sources}")
    _LOGGER.info(f"Solver identified.. {solver}")

    return unresolved_packages, package_version, sources, solver
