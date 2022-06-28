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

from thoth.investigator.configuration import Configuration

from .metrics_inspection_completed import inspection_completed_exceptions
from .metrics_inspection_completed import inspection_completed_in_progress
from .metrics_inspection_completed import inspection_completed_success
from ..common import register_handler, wait_for_limit

from thoth.common import OpenShift

from thoth.messaging.inspection_complete import inspection_completed_message

from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(inspection_completed_message.topic_name, ["v1"])
@count_exceptions(inspection_completed_exceptions)
@track_inprogress(inspection_completed_in_progress)
async def parse_inspection_completed(inspection_completed: Dict[str, Any], openshift: OpenShift, **kwargs):
    """Schedule graph sync for inspection after completion."""
    await wait_for_limit(openshift=openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
    workflow_name = openshift.schedule_graph_sync(
        inspection_completed["inspection_id"], force_sync=inspection_completed["force_sync"]
    )

    _LOGGER.debug(f"Graph sync workflow, {workflow_name}, for inspection {inspection_completed['inspection_id']}")
    inspection_completed_success.inc()
