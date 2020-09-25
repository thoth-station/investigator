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

"""Investigate message to schedule qebhwt."""

import logging

from thoth.common import OpenShift
from thoth.messaging import QebHwtTriggerMessage

from ..common import wait_for_limit

from .metrics_qebhwt_trigger import qebhwt_trigger_exceptions
from .metrics_qebhwt_trigger import qebhwt_trigger_in_progress
from .metrics_qebhwt_trigger import qebhwt_trigger_success

_LOGGER = logging.getLogger(__name__)


@qebhwt_trigger_exceptions.count_exceptions()
@qebhwt_trigger_in_progress.track_inprogress()
async def parse_qebhwt_trigger_message(qebhwt_trigger: QebHwtTriggerMessage, openshift: OpenShift) -> None:
    """Parse qebhwt_trigger message."""
    await wait_for_limit(openshift)
    workflow_name = openshift.schedule_qebhwt_workflow(
        github_event_type=qebhwt_trigger.github_event_type,
        github_check_run_id=qebhwt_trigger.github_check_run_id,
        github_installation_id=qebhwt_trigger.github_installation_id,
        github_base_repo_url=qebhwt_trigger.github_base_repo_url,
        github_head_repo_url=qebhwt_trigger.github_head_repo_url,
        origin=qebhwt_trigger.origin,
        revision=qebhwt_trigger.revision,
        host=qebhwt_trigger.host,
        job_id=qebhwt_trigger.job_id,
    )
    _LOGGER.debug(f"Scheduled qebhwt workflow {workflow_name}")
    qebhwt_trigger_success.inc()
