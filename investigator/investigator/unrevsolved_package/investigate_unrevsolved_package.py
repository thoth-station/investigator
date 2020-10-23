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

"""This file contains methods used by Thoth investigator to investigate on unrevsolved packages."""

import logging
from typing import Dict, Any

from thoth.messaging import UnrevsolvedPackageMessage
from thoth.common import OpenShift

from .. import common
from ..configuration import Configuration
from ..metrics import scheduled_workflows
from ..common import register_handler
from .metrics_unrevsolved_package import unrevsolved_package_exceptions
from .metrics_unrevsolved_package import unrevsolved_package_in_progress
from .metrics_unrevsolved_package import unrevsolved_package_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@count_exceptions(unrevsolved_package_exceptions)
@track_inprogress(unrevsolved_package_in_progress)
@register_handler(UnrevsolvedPackageMessage().topic_name, ["v1"])
async def parse_revsolved_package_message(unrevsolved_package: Dict[str, Any], openshift: OpenShift) -> None:
    """Parse soolved package message."""
    package_name = unrevsolved_package["package_name"]
    package_version = unrevsolved_package["package_version"]

    # Revsolver logic
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER:
        revsolver_wfs_scheduled, _ = await common.learn_using_revsolver(
            openshift=openshift,
            is_present=True,
            package_name=package_name,
            package_version=package_version,
            revsolver_packages_seen=[],
        )

        scheduled_workflows.labels(message_type=UnrevsolvedPackageMessage.base_name, workflow_type="revsolver").inc(
            revsolver_wfs_scheduled
        )

    unrevsolved_package_success.inc()
