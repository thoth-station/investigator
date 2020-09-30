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

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.messaging import PackageReleasedMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from .. import common
from .metrics_package_released import package_released_exceptions
from .metrics_package_released import package_released_in_progress
from .metrics_package_released import package_released_success


@package_released_exceptions.count_exceptions()
@package_released_in_progress.track_inprogress()
async def parse_package_released_message(
    package_released: MessageBase, openshift: OpenShift, graph: GraphDatabase
) -> None:
    """Parse package released message."""
    package_name = package_released.package_name
    package_version = package_released.package_version
    index_url = package_released.index_url

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

        scheduled_workflows.labels(message_type=PackageReleasedMessage.topic_name, workflow_type="solver").inc(
            solver_wf_scheduled
        )


    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER:
        # Revsolver logic
        revsolver_wf_scheduled, _ = await common.learn_using_revsolver(
            openshift=openshift, is_present=False, package_name=package_name, package_version=package_version,
        )

        scheduled_workflows.labels(message_type=PackageReleasedMessage.topic_name, workflow_type="revsolver").inc(
            revsolver_wf_scheduled
        )

    package_released_success.inc()
