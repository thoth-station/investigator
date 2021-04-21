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

from .metrics_missing_package import missing_package_exceptions
from .metrics_missing_package import missing_package_success
from .metrics_missing_package import missing_package_in_progress
from ..common import register_handler

# from ..metrics import scheduled_workflows

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import missing_package_message


@register_handler(missing_package_message.topic_name, ["v1"])
@count_exceptions(missing_package_exceptions)
@track_inprogress(missing_package_in_progress)
async def parse_missing_package(package: Dict[str, Any], **kwargs):
    """Process a missing package message from package-update producer."""
    # TODO call kebechet with the missing package name, which would call kebechet on the individual
    # repositories with a different subcommand that would just create an issue.

    # scheduled_workflows.labels(
    #     message_type=MissingPackageMessage.base_name, workflow_type="kebechet-administrator"
    # ).inc()

    missing_package_success.inc()
