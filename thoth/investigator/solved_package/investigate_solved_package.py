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

"""This file contains methods used by Thoth investigator to investigate on solved packages."""

import logging
from typing import Dict, Any

from thoth.storages.graph import GraphDatabase
from thoth.messaging import SolvedPackageMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from .. import common
from ..configuration import Configuration
from ..common import register_handler

from .metrics_solved_package import solved_package_exceptions
from .metrics_solved_package import solved_package_success
from .metrics_solved_package import solved_package_in_progress
from prometheus_async.aio import count_exceptions, track_inprogress

_LOGGER = logging.getLogger(__name__)


@register_handler(SolvedPackageMessage().topic_name, ["v1"])
@count_exceptions(solved_package_exceptions)
@track_inprogress(solved_package_in_progress)
async def parse_solved_package_message(
    solved_package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs
) -> None:
    """Parse solved package message."""
    package_name = solved_package["package_name"]
    package_version = solved_package["package_version"]
    index_url: str = solved_package["index_url"]

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY:
        # SI logic
        si_wfs_scheduled = await common.learn_about_security(
            openshift=openshift,
            graph=graph,
            is_present=True,
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
        )

        scheduled_workflows.labels(message_type=SolvedPackageMessage.base_name, workflow_type="security-indicator").inc(
            si_wfs_scheduled
        )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        # Schedule Kebechet Administrator
        message_info = {
            "PACKAGE_NAME": package_name,
            "THOTH_PACKAGE_VERSION": package_version,
            "THOTH_PACKAGE_INDEX": index_url,
            "SOLVER_NAME": solved_package.get("solver"),  # We pass the solver name also.
        }

        # We schedule Kebechet Administrator workflow here -
        workflow_id = await common.schedule_kebechet_administrator(
            openshift=openshift, message_info=message_info, message_name=SolvedPackageMessage.__name__,
        )
        _LOGGER.info(f"Schedule Kebechet Administrator with id = {workflow_id}")
        scheduled_workflows.labels(
            message_type=SolvedPackageMessage.base_name, workflow_type="kebechet-administrator"
        ).inc()

    solved_package_success.inc()
