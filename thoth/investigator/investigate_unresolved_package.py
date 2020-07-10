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

from typing import Optional, Dict, Any, List, Union
from pathlib import Path

from thoth.storages.graph import GraphDatabase
from thoth.common import OpenShift
from thoth.python import Pipfile
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

prometheus_registry = CollectorRegistry()

_LOGGER = logging.getLogger(__name__)

_OPENSHIFT = OpenShift()

_GRAPH = GraphDatabase()

_METRIC_UNRESOLVED_TYPE = Gauge(
    "thoth_unresolved_package", "Unresolved package scheduled info.", ["package_name"], registry=prometheus_registry
)

_THOTH_METRICS_PUSHGATEWAY_URL = os.getenv(
    "PROMETHEUS_PUSHGATEWAY_URL", "pushgateway-dh-prod-monitoring.cloud.datahub.psi.redhat.com:80"
)


def investigate_unresolved_package(file_test_path: Optional[Path] = None) -> Union[Dict[str, Any], str]:
    """Investigate on possible unresolved packages."""
    if file_test_path:
        _LOGGER.debug("Dry run..")
        adviser_run_path = file_test_path
    else:
        adviser_run_path = os.environ["JSON_FILE_PATH"]

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

    parameters = content["result"]["parameters"]
    runtime_environment = parameters["project"].get("runtime_environment")

    solver = _OPENSHIFT.obtain_solver_from_runtime_environment(runtime_environment=runtime_environment)

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

    return packages_to_solve, solver


def parse_unresolved_package_message(unresolved_package: Dict[str, Any]) -> None:
    """Parse unresolved package message."""
    package_name = unresolved_package.package_name
    package_version = unresolved_package.package_version
    indexes = unresolved_package.sources
    solver = unresolved_package.solver

    registered_indexes = _GRAPH.get_python_package_index_urls_all()

    if any(index_url for index_url in indexes not in registered_indexes):
        _LOGGER.warning("User requested index that is not registered in Thoth.")

    if not package_version:
        packages = package_name
    else:
        packages = f"{package_name}==={package_version}"

    is_scheduled = _schedule_solver_with_priority(packages=packages, indexes=registered_indexes, solver=solver)

    # TODO: Expose metrics instead of sending to Pushgateway
    send_metrics_to_pushgateway(unresolved_package=unresolved_package, is_scheduled=is_scheduled)


def _schedule_solver_with_priority(packages: str, indexes: List[str], solver: str) -> int:
    """Schedule solver with priority."""
    try:
        analysis_id = _OPENSHIFT.schedule_solver(solver=solver, packages=packages, indexes=indexes, transitive=False)
        _LOGGER.info(
            "Scheduled solver %r for packages %r from indexes %r, analysis is %r",
            solver,
            packages,
            indexes,
            analysis_id,
        )
        is_scheduled = 1
    except Exception:
        _LOGGER.warning(f"Failed to schedule solver for package {packages} from {indexes}")
        is_scheduled = 0

    return is_scheduled


def send_metrics_to_pushgateway(unresolved_package: Dict[str, Any], is_scheduled: int) -> None:
    """Send metrics to Pushgateway."""
    _METRIC_UNRESOLVED_TYPE.labels(package_name=unresolved_package.package_name).set(is_scheduled)
    _LOGGER.info("unresolved_package(%r)=%r", unresolved_package.package_name, is_scheduled)

    if _THOTH_METRICS_PUSHGATEWAY_URL:
        try:
            _LOGGER.info(f"Submitting metrics to Prometheus pushgateway {_THOTH_METRICS_PUSHGATEWAY_URL}")
            push_to_gateway(
                _THOTH_METRICS_PUSHGATEWAY_URL, job="unresolved-package-priority", registry=prometheus_registry
            )
        except Exception as e:
            _LOGGER.info(f"An error occurred pushing the metrics: {str(e)}")
