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

"""Investigate message to schedule provenance checker."""

import logging
from typing import Dict, Any

from thoth.messaging import provenance_checker_trigger_message
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler
from ..configuration import Configuration

from .metrics_provenance_checker_trigger import provenance_checker_trigger_exceptions
from .metrics_provenance_checker_trigger import provenance_checker_trigger_in_progress
from .metrics_provenance_checker_trigger import provenance_checker_trigger_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(provenance_checker_trigger_message.topic_name, ["v1", "v2", "v3", "v4"])
@count_exceptions(provenance_checker_trigger_exceptions)
@track_inprogress(provenance_checker_trigger_in_progress)
async def parse_provenance_checker_trigger_message(
    provenance_checker_trigger: Dict[str, Any], openshift: OpenShift, **kwargs
) -> None:
    """Parse provenance_checker_trigger message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
    workflow_name = openshift.schedule_provenance_checker(
        origin=provenance_checker_trigger["origin"],
        authenticated=provenance_checker_trigger.get("authenticated", False),
        whitelisted_sources=provenance_checker_trigger["whitelisted_sources"],
        debug=provenance_checker_trigger["debug"],
        job_id=provenance_checker_trigger["job_id"],
        kebechet_metadata=provenance_checker_trigger.get("kebechet_metadata"),
        stack_info=provenance_checker_trigger.get("stack_info"),
        justification=provenance_checker_trigger.get("justification"),
    )
    _LOGGER.debug(f"Scheduled provenance checker workflow {workflow_name}")
    provenance_checker_trigger_success.inc()
