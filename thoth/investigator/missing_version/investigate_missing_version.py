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

"""Logic for handling hash_version message."""

import logging
from typing import Dict, Any

from ..common import schedule_kebechet_administrator, register_handler
from ..metrics import scheduled_workflows

from .metrics_missing_version import missing_version_exceptions
from .metrics_missing_version import missing_version_in_progress
from .metrics_missing_version import missing_version_success

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import missing_version_message
from thoth.common import OpenShift
from thoth.storages import GraphDatabase
from ..configuration import Configuration

_LOGGER = logging.getLogger(__name__)


@register_handler(missing_version_message.topic_name, ["v1"])
@count_exceptions(missing_version_exceptions)
@track_inprogress(missing_version_in_progress)
async def parse_missing_version(version: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs):
    """Process a missing version message from package-update producer."""
    graph.update_missing_flag_package_version(
        index_url=version["index_url"],
        package_name=version["package_name"],
        package_version=version["package_version"],
        value=True,
    )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        message_info = {
            "PACKAGE_NAME": version["package_name"],
            "THOTH_PACKAGE_VERSION": version["package_version"],
            "THOTH_PACKAGE_INDEX": version["index_url"],
        }

        # We schedule Kebechet Administrator workflow here -
        workflow_id = await schedule_kebechet_administrator(
            openshift=openshift, message_info=message_info, message_name=missing_version_message.base_name,
        )

        _LOGGER.info(f"Scheduled kebechet administrator workflow {workflow_id}")

        scheduled_workflows.labels(
            message_type=missing_version_message.base_name, workflow_type="kebechet-administrator"
        ).inc()
    missing_version_success.inc()
