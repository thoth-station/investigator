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

"""Investigate message to re schedule adviser."""

import logging

from thoth.messaging import MessageBase
from thoth.messaging import AdviserReRunMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from ..common import wait_for_limit
from ..configuration import Configuration

from .metrics_adviser_re_run import adviser_re_run_exceptions
from .metrics_adviser_re_run import adviser_re_run_success
from .metrics_adviser_re_run import adviser_re_run_in_progress
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@count_exceptions(adviser_re_run_exceptions)
@track_inprogress(adviser_re_run_in_progress)
async def parse_adviser_re_run_message(adviser_re_run: MessageBase, openshift: OpenShift) -> None:
    """Parse adviser re run message."""
    adviser_wfs_scheduled = await _re_schedule_adviser(openshift=openshift, parameters=adviser_re_run,)

    scheduled_workflows.labels(message_type=AdviserReRunMessage.topic_name, workflow_type="adviser").inc(
        adviser_wfs_scheduled
    )

    adviser_re_run_success.inc()


async def _re_schedule_adviser(openshift: OpenShift, parameters: MessageBase) -> int:
    """Re-Schedule Adviser."""
    re_run_adviser_id = parameters.adviser_id
    application_stack = parameters.application_stack
    recommendation_type = parameters.recommendation_type
    runtime_environment = parameters.runtime_environment
    origin = parameters.origin
    github_event_type = parameters.github_event_type
    github_check_run_id = parameters.github_check_run_id
    github_installation_id = parameters.github_installation_id
    github_base_repo_url = parameters.github_base_repo_url
    source_type = parameters.source_type

    try:
        await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
        analysis_id = openshift.schedule_adviser(
            application_stack=application_stack,
            recommendation_type=recommendation_type,
            runtime_environment=runtime_environment,
            origin=origin,
            github_event_type=github_event_type,
            github_check_run_id=github_check_run_id,
            github_installation_id=github_installation_id,
            github_base_repo_url=github_base_repo_url,
            re_run_adviser_id=re_run_adviser_id,
            source_type=source_type,
        )

        _LOGGER.info(
            "Re Scheduled Adviser for `failed` adviser run %r, analysis is %r", re_run_adviser_id, analysis_id,
        )
        is_scheduled = 1
    except Exception as e:
        _LOGGER.exception(f"Failed to schedule Adviser for `failed` adviser run {re_run_adviser_id}: {e}")
        is_scheduled = 0

    return is_scheduled
