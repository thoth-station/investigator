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


"""This is Thoth investigator common methods."""

import logging
from math import inf
from asyncio import sleep
import json
import os
from typing import List, Tuple, Optional, Callable
import yaml

from .github_service import GithubService

from thoth.common import OpenShift
from thoth.common.enums import ThothAdviserIntegrationEnum
from thoth.storages import GraphDatabase
from thoth.messaging import ALL_MESSAGES
from thamos import lib as thamos_lib

from .configuration import Configuration
from .metrics import message_version_metric

_LOGGER = logging.getLogger(__name__)


def _create_base_handler_table():
    table = dict()
    for i in ALL_MESSAGES:
        table[i.topic_name] = dict()
    return table


def _get_class_from_topic_name(topic_name):
    for i in ALL_MESSAGES:
        if i.topic_name == topic_name:
            return i


def _get_class_from_base_name(base_name):
    for i in ALL_MESSAGES:
        if i.base_name == base_name:
            return i


def _message_type_from_message_class(message_class):
    message_type = message_class.base_name.rsplit(".", maxsplit=1)[-1]  # type: str
    message_type = message_type.replace("-", "_")  # this is to match the metrics associate with processing
    return message_type


investigator_handler_table = _create_base_handler_table()
metrics_handler_table = _create_base_handler_table()


def register_handler(topic_name: str, version_strings: List[str], handler_table: dict = investigator_handler_table):
    """Register function to specific message versions."""

    def wrapper_func(func: Callable):
        for v in version_strings:
            handler_table[topic_name][v] = func
            _LOGGER.debug("Registering handler for %s==%s", topic_name, v)

        async def innner_func(*args, **kwargs):
            return await func(*args, **kwargs)

        return innner_func

    return wrapper_func


async def default_metric_handler(contents, msg, **kwargs):
    """Increments counter specific to message type and version that was encountered."""
    metric = message_version_metric.labels(
        message_type=_message_type_from_message_class(_get_class_from_topic_name(msg.topic())),
        message_version=json.loads(msg.value().decode("utf-8")).get("version", "None"),
    )
    metric.inc()


async def wait_for_limit(openshift: OpenShift, workflow_namespace: str):
    """Wait for pending workflow limit."""
    total_pending = inf
    if Configuration.PENDING_WORKFLOW_LIMIT is None:
        return
    limit = int(Configuration.PENDING_WORKFLOW_LIMIT)
    total_pending = openshift.workflow_manager.get_pending_workflows(workflow_namespace=workflow_namespace)
    _LOGGER.debug("Current number pending = %d", total_pending)
    while total_pending > limit:
        await sleep(Configuration.SLEEP_TIME)
        total_pending = openshift.workflow_manager.get_pending_workflows(workflow_namespace=workflow_namespace)
        _LOGGER.debug("Current number pending = %d", total_pending)


async def learn_about_security(
    openshift: OpenShift,
    graph: GraphDatabase,
    is_present: bool,
    package_name: str,
    index_url: str,
    package_version: str,
) -> int:
    """Learn about security of Package Version Index."""
    if is_present:
        # Check if package version index has been already analyzed for security
        is_analyzed = graph.si_aggregated_python_package_version_exists(
            package_name=package_name, package_version=package_version, index_url=index_url
        )

        if is_analyzed:
            return 0

    # Package never seen (schedule si workflow to collect knowledge for Thoth)
    is_si_analyzer_scheduled = await _schedule_security_indicator(
        openshift=openshift, package_name=package_name, package_version=package_version, index_url=index_url
    )

    return is_si_analyzer_scheduled


async def _schedule_security_indicator(
    openshift: OpenShift, package_name: str, package_version: str, index_url: str
) -> int:
    """Schedule Security Indicator."""
    try:
        await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
        analysis_id = openshift.schedule_security_indicator(
            python_package_name=package_name,
            python_package_version=package_version,
            python_package_index=index_url,
            aggregation_function="process_data",
        )
        _LOGGER.info(
            "Scheduled SI workflow for package %r in version %r from index %r, analysis is %r",
            package_name,
            package_version,
            index_url,
            analysis_id,
        )
        is_scheduled = 1
    except Exception as e:
        _LOGGER.exception(
            f"Failed to schedule SI for package {package_name} in version {package_version} from index {index_url}: {e}"
        )
        raise e

    return is_scheduled


async def learn_using_revsolver(
    openshift: OpenShift,
    is_present: bool,
    package_name: str,
    package_version: str,
    revsolver_packages_seen: Optional[List[Tuple[str, str]]] = None,
) -> Tuple[int, List[Tuple[str, str]]]:
    """Learn using revsolver about Package Version dependencies."""
    revsolver_packages_seen = revsolver_packages_seen or []
    if not is_present and (package_name, package_version) not in revsolver_packages_seen:
        # Package never seen (schedule revsolver workflow to collect knowledge for Thoth)
        is_revsolver_scheduled = await _schedule_revsolver(
            openshift=openshift, package_name=package_name, package_version=package_version
        )
        revsolver_packages_seen.append((package_name, package_version))

        return is_revsolver_scheduled, revsolver_packages_seen

    return 0, revsolver_packages_seen


async def _schedule_revsolver(openshift: OpenShift, package_name: str, package_version: str) -> int:
    """Schedule revsolver."""
    try:
        await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
        analysis_id = openshift.schedule_revsolver(
            package_name=package_name, package_version=package_version, debug=Configuration.LOG_REVSOLVER
        )
        _LOGGER.info(
            "Scheduled reverse solver for package %r in version %r, analysis is %r",
            package_name,
            package_version,
            analysis_id,
        )
        is_scheduled = 1
    except Exception as e:
        _LOGGER.exception(
            "Failed to schedule reverse solver for %r in version %r: %r", package_name, package_version, e
        )
        raise e

    return is_scheduled


async def learn_using_solver(
    openshift: OpenShift,
    graph: GraphDatabase,
    is_present: bool,
    package_name: str,
    index_url: str,
    package_version: str,
    solver: Optional[str] = None,
) -> int:
    """Learn using solver about Package Version Index dependencies."""
    if not is_present:
        # Package never seen (schedule all solver workflows to collect all knowledge for Thoth)
        are_solvers_scheduled = await _schedule_all_solvers(
            openshift=openshift, package_name=package_name, package_version=package_version, indexes=[index_url]
        )
        return are_solvers_scheduled

    # Select solvers
    if not solver:
        solvers: List[str] = openshift.get_solver_names()
    else:
        solvers = [solver]

    dependency_indexes = graph.get_python_package_index_urls_all(enabled=True)

    # Check for which solver has not been solved and schedule solver workflow
    are_solvers_scheduled = 0

    for solver_name in solvers:
        is_solved = graph.python_package_version_exists(
            package_name=package_name, package_version=package_version, index_url=index_url, solver_name=solver_name
        )

        if not is_solved:

            is_solver_scheduled = _schedule_solver(
                openshift=openshift,
                package_name=package_name,
                package_version=package_version,
                indexes=[index_url],
                dependency_indexes=dependency_indexes,
                solver_name=solver_name,
            )

            are_solvers_scheduled += is_solver_scheduled

    return are_solvers_scheduled


def _schedule_solver(
    openshift: OpenShift,
    package_name: str,
    package_version: str,
    dependency_indexes: List[str],
    indexes: List[str],
    solver_name: str,
) -> int:
    """Schedule solver."""
    packages = f"{package_name}==={package_version}"

    try:
        # mypy is throwing errors in CI without this ignore
        analysis_id = openshift.schedule_solver(  # type: ignore
            solver=solver_name,
            packages=packages,
            indexes=indexes,
            dependency_indexes=dependency_indexes,
            transitive=False,
            debug=Configuration.LOG_SOLVER,
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
        _LOGGER.exception(f"Failed to schedule solver {solver_name} for package {packages} from {indexes}: {e}")
        raise e

    return is_scheduled


async def _schedule_all_solvers(
    openshift: OpenShift, package_name: str, package_version: str, indexes: List[str]
) -> int:
    """Schedule all solvers."""
    packages = f"{package_name}==={package_version}"

    try:
        await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
        analysis_ids = openshift.schedule_all_solvers(packages=packages, indexes=indexes)
        _LOGGER.info(
            "Scheduled solvers for packages %r from indexes %r, analysis ids are %r", packages, indexes, analysis_ids
        )
        are_scheduled = len(analysis_ids)
    except Exception as e:
        _LOGGER.exception(f"Failed to schedule solvers for package {packages} from {indexes}: {e}")
        raise e

    return are_scheduled


async def send_advise_request_for_installation(
    slug: str, environment_name: str, keb_meta: dict, gh_service: GithubService
):
    """Send a request to Thoth user-api for a given runtime environment.

    args:
        slug (str): '<namespace>/<repo_name>'
        environment_name (str): runtime environment name as it appears in .thoth.yaml
        keb_meta (dict): meta data which indicates which internal trigger caused the request
        gh_service (GithubService): GithubService instance for interacting with Github api
    returns:
        bool: returns true if the request was sent and false if it was not sent
    """
    namespace, repo = slug.split("/")
    project = gh_service.get_project(namespace=namespace, repo=repo)
    thoth_config = await project.get_file(".thoth.yaml")
    thoth_config = yaml.safe_load(thoth_config)
    overlay_dir = thoth_config.get("overlays_dir", "")
    if not overlay_dir and thoth_config["runtime_environments"][0]["name"] != environment_name:
        return False  # if no overlay present, only the first entry of environments should be acted on
    for r_e in thoth_config["runtime_environments"]:
        if r_e["name"] == environment_name:
            runtime_environment = r_e
            break
    else:
        return False  # runtime environment is no longer present in config file, do not run adviser

    directory = os.path.join(overlay_dir, environment_name) if overlay_dir else ""
    # TODO: use thoth_config["requirements_format"] to hand other types of requirements files
    pipfile_path = os.path.join(directory, "Pipfile")
    pipfile_lock_path = os.path.join(directory, "Pipfile.lock")
    pipfile = await project.get_file(pipfile_path)
    pipfile_lock = await project.get_file(pipfile_lock_path)

    # THAMOS_TOKEN env variable must be set because kebechet_metadata is protected
    thamos_lib.advise(
        pipfile=pipfile,
        pipfile_lock=pipfile_lock,
        recommendation_type=thoth_config.get("recommendation_type"),
        runtime_environment=runtime_environment,
        no_static_analysis=True,
        nowait=True,
        origin=f"https://github.com/{slug}",
        source_type=ThothAdviserIntegrationEnum.KEBECHET,
        kebechet_metadata=keb_meta,
    )
    print("SUCCESS")
    return True
