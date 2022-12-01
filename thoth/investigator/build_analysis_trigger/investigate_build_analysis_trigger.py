#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2021 Fridolin Pokorny
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

"""Investigate message to schedule build analysis."""

import logging
from typing import Dict, Any

from thoth.messaging import build_analysis_trigger_message
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler, middletier_handlers
from ..configuration import Configuration

from .metrics_build_analysis_trigger import build_analysis_trigger_exceptions
from .metrics_build_analysis_trigger import build_analysis_trigger_in_progress
from .metrics_build_analysis_trigger import build_analysis_trigger_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(build_analysis_trigger_message.topic_name, ["v1"], middletier_handlers)
@count_exceptions(build_analysis_trigger_exceptions)
@track_inprogress(build_analysis_trigger_in_progress)
async def parse_build_analysis_trigger_message(
    build_analysis_trigger: Dict[str, Any], openshift: OpenShift, **kwargs
) -> None:
    """Parse build_analysis trigger message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
    workflow_id = openshift.schedule_build_analysis(
        base_image=build_analysis_trigger["base_image"],
        base_image_analysis_id=build_analysis_trigger["base_image_analysis_id"],
        base_registry_password=build_analysis_trigger["base_registry_password"],
        base_registry_user=build_analysis_trigger["base_registry_user"],
        base_registry_verify_tls=build_analysis_trigger["base_registry_verify_tls"],
        output_image=build_analysis_trigger["output_image"],
        output_image_analysis_id=build_analysis_trigger["output_image_analysis_id"],
        output_registry_password=build_analysis_trigger["output_registry_password"],
        output_registry_user=build_analysis_trigger["output_registry_user"],
        output_registry_verify_tls=build_analysis_trigger["output_registry_verify_tls"],
        buildlog_document_id=build_analysis_trigger["buildlog_document_id"],
        buildlog_parser_id=build_analysis_trigger["buildlog_parser_id"],
        environment_type=build_analysis_trigger["environment_type"],
        origin=build_analysis_trigger["origin"],
        debug=build_analysis_trigger["debug"],
        job_id=build_analysis_trigger["job_id"],
    )
    _LOGGER.debug(f"Scheduled build analysis workflow {workflow_id}")
    build_analysis_trigger_success.inc()
