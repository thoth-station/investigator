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

"""Logic for handling cve provided message."""

import logging
from typing import Dict, Any

from ..common import schedule_kebechet_administrator, register_handler
from ..configuration import Configuration
from ..metrics import scheduled_workflows

from .metrics_cve_provided import cve_provided_exceptions
from .metrics_cve_provided import cve_provided_success
from .metrics_cve_provided import cve_provided_in_progress
from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import cve_provided_message
from thoth.common import OpenShift

_LOGGER = logging.getLogger(__name__)


@register_handler(cve_provided_message.topic_name, ["v1"])
@count_exceptions(cve_provided_exceptions)
@track_inprogress(cve_provided_in_progress)
async def parse_cve_provided(cve_provided: Dict[str, Any], openshift: OpenShift, **kwargs):
    """Process a cve provided message."""
    # Add more logic if neccessary.

    # Schedule Kebechet administrator.
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        message_info = {
            "PACKAGE_NAME": cve_provided["package_name"],
            "THOTH_PACKAGE_VERSION": cve_provided["package_version"],
            "THOTH_PACKAGE_INDEX": cve_provided["index_url"],
        }

        # We schedule Kebechet Administrator workflow here -
        workflow_id = await schedule_kebechet_administrator(
            openshift=openshift,
            message_info=message_info,
            message_name=cve_provided_message.base_name,
        )

        scheduled_workflows.labels(
            message_type=cve_provided_message.base_name, workflow_type="kebechet-administrator"
        ).inc()
        _LOGGER.info(f"Scheduled kebechet administrator workflow {workflow_id}")

    cve_provided_success.inc()
