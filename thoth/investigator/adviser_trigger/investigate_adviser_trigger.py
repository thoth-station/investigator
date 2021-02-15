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

"""Investigate message to schedule adviser."""

import logging
from typing import Dict, Any

from thoth.messaging import AdviserTriggerMessage
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler
from ..configuration import Configuration

from .metrics_adviser_trigger import adviser_trigger_exceptions
from .metrics_adviser_trigger import adviser_trigger_in_progress
from .metrics_adviser_trigger import adviser_trigger_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(AdviserTriggerMessage().topic_name, ["v2"])
@count_exceptions(adviser_trigger_exceptions)
@track_inprogress(adviser_trigger_in_progress)
async def parse_adviser_trigger_message(adviser_trigger: Dict[str, Any], openshift: OpenShift, **kwargs) -> None:
    """Parse adviser trigger message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
    workflow_id = openshift.schedule_adviser(
        recommendation_type=adviser_trigger["recommendation_type"],
        count=adviser_trigger["count"],
        limit=adviser_trigger["limit"],
        origin=adviser_trigger["origin"],
        dev=adviser_trigger["dev"],
        debug=adviser_trigger["debug"],
        job_id=adviser_trigger["job_id"],
        github_event_type=adviser_trigger["github_event_type"],
        github_check_run_id=adviser_trigger["github_check_run_id"],
        github_installation_id=adviser_trigger["github_installation_id"],
        github_base_repo_url=adviser_trigger["github_base_repo_url"],
        re_run_adviser_id=adviser_trigger["re_run_adviser_id"],
        source_type=adviser_trigger["source_type"],
    )
    _LOGGER.debug(f"Scheduled adviser workflow {workflow_id}")
    adviser_trigger_success.inc()
