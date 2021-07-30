#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Kevin Postlethwait
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

"""Logic for handling hash_mismatch message."""

import logging
from typing import Dict, Any

from ..common import schedule_kebechet_administrator, learn_using_solver, register_handler
from ..configuration import Configuration
from ..metrics import scheduled_workflows

from .metrics_hash_mismatch import hash_mismatch_exceptions
from .metrics_hash_mismatch import hash_mismatch_success
from .metrics_hash_mismatch import hash_mismatch_in_progress
from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import hash_mismatch_message
from thoth.common import OpenShift
from thoth.storages import GraphDatabase

_LOGGER = logging.getLogger(__name__)


@register_handler(hash_mismatch_message.topic_name, ["v1"])
@count_exceptions(hash_mismatch_exceptions)
@track_inprogress(hash_mismatch_in_progress)
async def parse_hash_mismatch(mismatch: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs):
    """Process a hash mismatch message from package-update producer."""
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER:
        # Solver logic
        solver_wf_scheduled = await learn_using_solver(
            openshift=openshift,
            graph=graph,
            is_present=False,
            package_name=mismatch["package_name"],
            index_url=mismatch["index_url"],
            package_version=mismatch["package_version"],
        )

        scheduled_workflows.labels(message_type=hash_mismatch_message.base_name, workflow_type="solver").inc(
            solver_wf_scheduled
        )

    if mismatch["missing_from_source"] != []:
        for h in mismatch["missing_from_source"]:
            graph.update_python_package_hash_present_flag(
                package_name=mismatch["package_name"],
                package_version=mismatch["package_version"],
                index_url=mismatch["index_url"],
                sha256=h,
            )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        message_info = {
            "PACKAGE_NAME": mismatch["package_name"],
            "THOTH_PACKAGE_VERSION": mismatch["package_version"],
            "THOTH_PACKAGE_INDEX": mismatch["index_url"],
        }

        # We schedule Kebechet Administrator workflow here -
        workflow_id = await schedule_kebechet_administrator(
            openshift=openshift,
            message_info=message_info,
            message_name=hash_mismatch_message.__name__,
        )
        scheduled_workflows.labels(
            message_type=hash_mismatch_message.base_name, workflow_type="kebechet-administrator"
        ).inc()

        _LOGGER.info(f"Scheduled kebechet administrator workflow {workflow_id}")

    hash_mismatch_success.inc()
