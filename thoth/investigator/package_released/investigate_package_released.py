#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Bissenbay Dauletbayev
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

"""This file contains methods used by Thoth investigator to investigate on package released messages."""

from typing import Dict, Any

from thoth.storages.graph import GraphDatabase
from thoth.messaging import PackageReleasedMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from .. import common
from ..common import register_handler
from ..configuration import Configuration
from .metrics_package_released import package_released_exceptions
from .metrics_package_released import package_released_in_progress
from .metrics_package_released import package_released_success
from prometheus_async.aio import track_inprogress, count_exceptions


@count_exceptions(package_released_exceptions)
@track_inprogress(package_released_in_progress)
@register_handler(PackageReleasedMessage().topic_name, ["v1"])
async def parse_package_released_message(
    package_released: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs
) -> None:
    """Parse package released message."""
    package_name = package_released["package_name"]
    package_version = package_released["package_version"]
    index_url = package_released["index_url"]

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER:
        # Solver logic
        solver_wf_scheduled = await common.learn_using_solver(
            openshift=openshift,
            graph=graph,
            is_present=False,
            package_name=package_name,
            index_url=index_url,
            package_version=package_version,
        )

        scheduled_workflows.labels(message_type=PackageReleasedMessage.base_name, workflow_type="solver").inc(
            solver_wf_scheduled
        )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER:
        # Revsolver logic
        revsolver_wf_scheduled, _ = await common.learn_using_revsolver(
            openshift=openshift, is_present=False, package_name=package_name, package_version=package_version,
        )

        scheduled_workflows.labels(message_type=PackageReleasedMessage.base_name, workflow_type="revsolver").inc(
            revsolver_wf_scheduled
        )

    package_released_success.inc()
