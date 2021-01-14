#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Sai Sankar Gochhayat
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

"""Investigate message to schedule Kebechet."""

import logging
from typing import Dict, Any

from thoth.messaging import KebechetRunUrlTriggerMessage
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler
from ..configuration import Configuration

from .metrics_kebechet_run_url_trigger import kebechet_run_url_trigger_success
from .metrics_kebechet_run_url_trigger import kebechet_run_url_trigger_in_progress
from .metrics_kebechet_run_url_trigger import kebechet_run_url_trigger_exceptions
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(KebechetRunUrlTriggerMessage().topic_name, ["v1"])
@count_exceptions(kebechet_run_url_trigger_exceptions)
@track_inprogress(kebechet_run_url_trigger_in_progress)
async def parse_kebechet_run_url_trigger_message(
    kebechet_run_url_trigger: Dict[str, Any], openshift: OpenShift, **kwargs
) -> None:
    """Parse kebechet_run_url_trigger message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
    workflow_name = openshift.schedule_kebechet_run_url_workflow(
        repo_url=kebechet_run_url_trigger["url"],
        service_name=kebechet_run_url_trigger["service_name"],
        job_id=kebechet_run_url_trigger["job_id"],
    )
    _LOGGER.debug(f"Scheduled kebechet run url workflow {workflow_name}")
    kebechet_run_url_trigger_success.inc()
