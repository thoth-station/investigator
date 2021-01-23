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

"""Consume inspection complete message and schedule graph-sync."""

import logging
from typing import Dict, Any

from .metrics_inspection_complete import inspection_complete_exceptions
from .metrics_inspection_complete import inspection_complete_in_progress
from .metrics_inspection_complete import inspection_complete_success
from ..common import register_handler, wait_for_limit

from thoth.common import OpenShift

from thoth.messaging.inspection_complete import InspectionCompletedMessage

from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(InspectionCompletedMessage().topic_name, ["v1"])
@count_exceptions(inspection_complete_exceptions)
@track_inprogress(inspection_complete_in_progress)
async def parse_inspection_complete(inspection_complete: Dict[str, Any], openshift: OpenShift, **kwargs):
    """Retrieve adviser reports justifications."""
    wait_for_limit(openshift=openshift, workflow_namespace=openshift.middletier_namespace)
    workflow_name = openshift.schedule_graph_sync(
        inspection_complete["inspection_id"], force_sync=inspection_complete["force_sync"]
    )

    _LOGGER.debug(f"Graph sync workflow, {workflow_name}, for inspection {inspection_complete['inspection_id']}")
    inspection_complete_success.inc()
