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

"""Logic for handling missing_package message."""

from typing import Dict, Any
import logging

from .metrics_missing_package import missing_package_exceptions
from .metrics_missing_package import missing_package_success
from .metrics_missing_package import missing_package_in_progress
from ..common import register_handler, Configuration, schedule_kebechet_administrator

from ..metrics import scheduled_workflows

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import missing_package_message
from thoth.storages import GraphDatabase
from thoth.common import OpenShift

_LOGGER = logging.getLogger(__name__)


@register_handler(missing_package_message.topic_name, ["v1"])
@count_exceptions(missing_package_exceptions)
@track_inprogress(missing_package_in_progress)
async def parse_missing_package(package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs):
    """Process a missing package message from package-update producer."""
    python_package_versions = graph.get_python_package_versions_all(
        package_name=package["package_name"], index_url=package["index_url"], count=None,
    )

    for _, version, _ in python_package_versions:
        graph.update_missing_flag_package_version(
            package_name=package["package_name"], package_version=version, index_url=package["index_url"], value=True,
        )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        message_info = {
            "PACKAGE_NAME": version["package_name"],
            "THOTH_PACKAGE_INDEX": version["index_url"],
        }

        # We schedule Kebechet Administrator workflow here -
        workflow_id = await schedule_kebechet_administrator(
            openshift=openshift, message_info=message_info, message_name=missing_package_message.base_name,
        )

        _LOGGER.info(f"Scheduled kebechet administrator workflow {workflow_id}")

        scheduled_workflows.labels(
            message_type=missing_package_message.base_name, workflow_type="kebechet-administrator"
        ).inc()

    missing_package_success.inc()
