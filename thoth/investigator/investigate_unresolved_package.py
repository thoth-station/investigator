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

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.common import OpenShift
from thoth.python import Pipfile
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter

_LOG_SOLVER = os.environ.get("THOTH_LOG_SOLVER") == "DEBUG"
_LOG_REVSOLVER = os.environ.get("THOTH_LOG_REVSOLVER") == "DEBUG"

IN_PROGRESS_GAUGE = Gauge(
    "investigators_in_progress", "Total number of investigation messages currently being processed."
)
EXCEPTIONS_COUNTER = Counter(
    "investigator_exceptions", "Number of investigation messages which failed to be processed."
)
SUCCESSES_COUNTER = Counter(
    "investigators_processed", "Number of investigation messages which were successfully processed."
)

prometheus_registry = CollectorRegistry()

_LOGGER = logging.getLogger(__name__)

_METRIC_UNRESOLVED_TYPE = Gauge(
    "thoth_unresolved_package", "Unresolved package scheduled info.", ["package_name"], registry=prometheus_registry
)

_THOTH_METRICS_PUSHGATEWAY_URL = os.getenv(
    "PROMETHEUS_PUSHGATEWAY_URL", "pushgateway-dh-prod-monitoring.cloud.datahub.psi.redhat.com:80"
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

    solver = OpenShift.obtain_solver_from_runtime_environment(runtime_environment=runtime_environment)

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
    requested_indexes: Optional[List[str]] = unresolved_package.index_url
    solver = unresolved_package.solver

    openshift = OpenShift()

    graph = GraphDatabase()
    graph.connect()

    # Select indexes
    registered_indexes: List[str] = graph.get_python_package_index_urls_all()

    indexes = registered_indexes

    if not requested_indexes:
        _LOGGER.info("using Thoth registered indexes...")
    else:
        if all(index_url in registered_indexes for index_url in requested_indexes):
            indexes = requested_indexes
            _LOGGER.info("Using requested indexes...")
        else:
            _LOGGER.info("Using Thoth registered indexes...")

    # Select solvers
    if not solver:
        solvers: List[str] = openshift.get_solver_names()
    else:
        solvers = [solver]

    # Check package version for each index

    for index_url in indexes:

        is_present = graph.python_package_version_exists(
            package_name=package_name, package_version=package_version, index_url=index_url, solver_name=solver_name
        )

        if is_present:

            # Check for which solver has been already solved
            for solver_name in solvers:
                is_solved = graph.python_package_version_exists(
                    package_name=package_name,
                    package_version=package_version,
                    index_url=index_url,
                    solver_name=solver_name,
                )
                if not is_solved:
                    is_scheduled = _schedule_solver(
                        openshift=openshift,
                        package_name=package_name,
                        package_version=package_version,
                        indexes=[index_url],
                        solver_name=solver_name,
                    )

        else:
            are_scheduled = _schedule_all_solvers(
                package_name=package_name, package_version=package_version, indexes=[index_url]
            )

            is_revsolver_scheduled = _schedule_revsolver(package_name=package_name, package_version=package_version)

            is_si_analyzer_scheduled = _schedule_security_indicator(package_name=package_name, package_version=package_version, index_url=index_url)

    SUCCESSES_COUNTER.inc()


def _schedule_solver(
    openshift: Openshift, package_name: str, package_version: str, indexes: List[str], solver_name: str
) -> int:
    """Schedule solver."""
    try:
        if not package_version:
            packages = package_name
        else:
            packages = f"{package_name}==={package_version}"

        analysis_id = openshift.schedule_solver(
            solver=solver_name, packages=packages, indexes=indexes, transitive=False, debug=_LOG_SOLVER
        )
        _LOGGER.info(
            "Scheduled solver %r for packages %r from indexes %r, analysis is %r",
            solver_name,
            packages,
            indexes,
            analysis_id,
        )
        is_scheduled = 1
    except Exception as e:
        _LOGGER.warning(f"Failed to schedule solver {solver_name} for package {packages} from {indexes}: {e}")
        is_scheduled = 0

    return is_scheduled


def _schedule_all_solvers(openshift: OpenShift, package_name: str, package_version: str, indexes: List[str]) -> int:
    """Schedule all solvers."""
    try:
        analysis_ids = openshift.schedule_all_solvers(packages=f"{package_name}==={package_version}", indexes=indexes)
        _LOGGER.info(
            "Scheduled solver %r for packages %r from indexes %r, analysis is %r", packages, indexes, analysis_ids
        )
        are_scheduled = len(analysis_ids)
    except Exception:
        _LOGGER.warning(f"Failed to schedule solvers for package {packages} from {indexes}")
        are_scheduled = 0

    return are_scheduled


def _schedule_revsolver(openshift: OpenShift, package_name: str, package_version: str) -> int:
    """Schedule revsolver."""
    if package_version and (package_name, package_version) not in revsolver_packages_seen:
        try:
            analysis_id = openshift.schedule_revsolver(
                package_name=package_name, package_version=package_version, debug=_LOG_REVSOLVER
            )
            _LOGGER.info(
                "Scheduled reverse solver for package %r in version %r, analysis is %r",
                package_name,
                package_version,
                analysis_id,
            )
            is_scheduled = 1
        except Exception:
            _LOGGER.warning("Failed to schedule reverse solver for %r in version %r", package_name, package_version)
            is_scheduled = 0
            continue

    return is_scheduled

def _schedule_security_indicator(package_name: str, package_version: str, index_url: str) -> int:
    """Schedule Security Indicator."""
    openshift = OpenShift()
    try:
        analysis_id = openshift.schedule_security_indicator(
            python_package_name=package_name,
            python_package_version=package_version,
            python_package_index=index_url,
            aggregation_function="process_data",
        )
        _LOGGER.info(
            "Scheduled SI %r for package %r in version %r from index %r, analysis is %r",
            package_name,
            package_version,
            index_url,
            analysis_id,
        )
        is_scheduled = 1
    except Exception:
        _LOGGER.warning(
            f"Failed to schedule SI for package {package_name} in version {package_version} from index {index_url}"
        )
        is_scheduled = 0

    return is_scheduled
