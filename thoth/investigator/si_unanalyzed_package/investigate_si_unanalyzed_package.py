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

"""This file contains methods used by Thoth investigator to investigate on si unanalyzed packages."""

import logging
from typing import Dict, Any

from thoth.storages.graph import GraphDatabase
from thoth.messaging import si_unanalyzed_package_message
from thoth.common import OpenShift


from ..metrics import scheduled_workflows
from .. import common
from ..configuration import Configuration
from ..common import register_handler, middletier_handlers

from .metrics_si_unanalyzed_package import si_unanalyzed_package_in_progress
from .metrics_si_unanalyzed_package import si_unanalyzed_package_success
from .metrics_si_unanalyzed_package import si_unanalyzed_package_exceptions
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(si_unanalyzed_package_message.topic_name, ["v1"], middletier_handlers)
@count_exceptions(si_unanalyzed_package_exceptions)
@track_inprogress(si_unanalyzed_package_in_progress)
async def parse_si_unanalyzed_package_message(
    si_unanalyzed_package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, **kwargs
) -> None:
    """Parse SI Unanalyzed package messages."""
    package_name: str = si_unanalyzed_package["package_name"]
    package_version: str = si_unanalyzed_package["package_version"]
    index_url: str = si_unanalyzed_package["index_url"]

    # SI logic
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY:
        si_wfs_scheduled = await common.learn_about_security(
            openshift=openshift,
            graph=graph,
            is_present=True,
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
        )

        scheduled_workflows.labels(
            message_type=si_unanalyzed_package_message.base_name, workflow_type="security-indicator"
        ).inc(si_wfs_scheduled)

    si_unanalyzed_package_success.inc()
