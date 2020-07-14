#!/usr/bin/env python3
# thoth-investigator
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


"""This file contains methods used by Thoth investigator to investigate on unresolved packages."""


import sys
import logging
import json
import os

from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

from prometheus_client import Gauge, Counter

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.common import OpenShift
from thoth.python import Pipfile
from thoth.investigator.metrics import prometheus_registry


IN_PROGRESS_GAUGE = Gauge(
    "investigators_in_progress", "Total number of investigation messages currently being processed."
)
EXCEPTIONS_COUNTER = Counter(
    "investigator_exceptions", "Number of investigation messages which failed to be processed."
)
SUCCESSES_COUNTER = Counter(
    "investigators_processed", "Number of investigation messages which were successfully processed."
)


_LOGGER = logging.getLogger(__name__)


OPENSHIFT = OpenShift()


_METRIC_UNRESOLVED_TYPE = Gauge(
    "thoth_unresolved_package", "Unresolved package scheduled info.", ["package_name"], registry=prometheus_registry
)


def investigate_unresolved_package(file_test_path: Optional[Path] = None) -> Tuple[Dict[Any, Any], Optional[str]]:
    """Investigate on unresolved packages."""
    if file_test_path:
        _LOGGER.debug("Dry run..")
        adviser_run_path = file_test_path
    else:
        adviser_run_path = Path(os.environ["JSON_FILE_PATH"])

    if not adviser_run_path.exists():
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

    parameters = content["result"]["parameters"]
    runtime_environment = parameters["project"].get("runtime_environment")

    solver = OPENSHIFT.obtain_solver_from_runtime_environment(runtime_environment=runtime_environment)

    requirements = parameters["project"].get("requirements")

    pipfile = Pipfile.from_dict(requirements)
    packages = pipfile.packages.packages
    dev_packages = pipfile.dev_packages.packages

    packages_to_solve = {}
    for package_name in unresolved_packages:

        if package_name in packages:
            packages_to_solve[package_name] = packages[package_name]

        if package_name in dev_packages:
            packages_to_solve[package_name] = dev_packages[package_name]

    _LOGGER.info(f"Unresolved packages identified.. {packages_to_solve}")

    if solver:
        return (packages_to_solve, solver)

    return (packages_to_solve, None)


@EXCEPTIONS_COUNTER.count_exceptions()
@IN_PROGRESS_GAUGE.track_inprogress()
def parse_unresolved_package_message(unresolved_package: MessageBase) -> None:
    """Parse unresolved package message."""
    package_name = unresolved_package.package_name
    package_version = unresolved_package.package_version
    indexes: List[Any] = unresolved_package.index_url
    solver = unresolved_package.solver

    _graph = GraphDatabase()
    registered_indexes: List[Any] = _graph.get_python_package_index_urls_all()

    if set(indexes) & set(registered_indexes):
        _LOGGER.warning("User requested index that is not registered in Thoth.")

    if not package_version:
        packages = package_name
    else:
        packages = f"{package_name}==={package_version}"

    if _schedule_solver_with_priority(packages=packages, indexes=registered_indexes, solver=solver):
        SUCCESSES_COUNTER.inc()


def _schedule_solver_with_priority(packages: str, indexes: List[str], solver: str) -> bool:
    """Schedule solver with priority."""
    try:
        analysis_id = OPENSHIFT.schedule_solver(solver=solver, packages=packages, indexes=indexes, transitive=False)
        _LOGGER.info(
            "Scheduled solver %r for packages %r from indexes %r, analysis is %r",
            solver,
            packages,
            indexes,
            analysis_id,
        )
        return True

    except Exception:
        _LOGGER.warning(f"Failed to schedule solver for package {packages} from {indexes}")

    return False
