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

import logging

from typing import Optional, List, Dict, Any

from thoth.storages.graph import GraphDatabase
from thoth.messaging import unresolved_package_message
from thoth.common import OpenShift
from thoth.python import Source

from ..metrics import scheduled_workflows
from .. import common
from ..configuration import Configuration
from ..common import register_handler, middletier_handlers

from .metrics_unresolved_package import unresolved_package_exceptions
from .metrics_unresolved_package import unresolved_package_in_progress
from .metrics_unresolved_package import unresolved_package_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(unresolved_package_message.topic_name, ["v1"], middletier_handlers)
@count_exceptions(unresolved_package_exceptions)
@track_inprogress(unresolved_package_in_progress)
async def parse_unresolved_package_message(
    unresolved_package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs
) -> None:
    """Parse unresolved package message."""
    package_name = unresolved_package["package_name"]
    package_version = unresolved_package["package_version"]
    requested_index: Optional[str] = unresolved_package["index_url"]
    solver = unresolved_package["solver"]

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER:
        total_solver_wfs_scheduled = 0

        # Select indexes
        registered_indexes: List[str] = graph.get_python_package_index_urls_all()

        if requested_index not in registered_indexes:
            error_message = f"Requested index {requested_index} is not registered in Thoth"
            raise ValueError(error_message)

        versions = _check_package_version(
            package_name=package_name, package_version=package_version, index_url=requested_index
        )

        # Loop versions from the latest one
        for version in versions:

            # Check if package version index exists in Thoth Knowledge Graph
            is_present = graph.python_package_version_exists(
                package_name=package_name, package_version=version, index_url=requested_index
            )

            # Solver logic
            solver_wfs_scheduled = await common.learn_using_solver(
                openshift=openshift,
                graph=graph,
                is_present=is_present,
                package_name=package_name,
                index_url=requested_index,
                package_version=version,
                solver=solver,
            )

            total_solver_wfs_scheduled += solver_wfs_scheduled

        scheduled_workflows.labels(message_type=unresolved_package_message.base_name, workflow_type="solver").inc(
            total_solver_wfs_scheduled
        )

    unresolved_package_success.inc()


def _check_package_version(package_name: str, package_version: Optional[str], index_url: str) -> List[str]:
    """Check package version."""
    versions = []

    if not package_version or package_version == "*":
        _LOGGER.debug("consider index %r", index_url)
        source = Source(index_url)

        try:
            # Get sorted versions (latest first -> latest = versions[0])
            if package_versions := source.get_sorted_package_versions(package_name):
                versions = list(map(str, package_versions))
            else:
                versions = []

        except Exception as exc:
            _LOGGER.warning(
                f"Could not retrieve versions for package {package_name} from index {index_url}: {str(exc)}"
            )

    else:
        versions.append(package_version)

    return versions
