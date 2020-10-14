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

"""Investigate message to schedule kebechet."""

import logging
from typing import Dict, Any

from thoth.messaging import KebechetTriggerMessage
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler
from ..configuration import Configuration
from .metrics_kebechet_trigger import kebechet_trigger_exceptions
from .metrics_kebechet_trigger import kebechet_trigger_in_progress
from .metrics_kebechet_trigger import kebechet_trigger_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@count_exceptions(kebechet_trigger_exceptions)
@track_inprogress(kebechet_trigger_in_progress)
@register_handler(KebechetTriggerMessage().topic_name, ["v1"])
async def parse_kebechet_trigger_message(kebechet_trigger: Dict[str, Any], openshift: OpenShift) -> None:
    """Parse kebechet_trigger message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
    workflow_name = openshift.schedule_kebechet_workflow(
        webhook_payload=kebechet_trigger["webhook_payload"], job_id=kebechet_trigger["job_id"],
    )
    _LOGGER.debug(f"Scheduled kebechet workflow {workflow_name}")
    kebechet_trigger_success.inc()
