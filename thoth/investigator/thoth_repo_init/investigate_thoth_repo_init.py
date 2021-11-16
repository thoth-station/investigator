#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2021 Kevin Postlethwait
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

"""Investigate message to schedule repo_init workflow."""

import logging
from typing import Dict, Any

from thoth.messaging import thoth_repo_init_message
from thoth.common import OpenShift

from ..common import wait_for_limit, register_handler
from ..configuration import Configuration

from .metrics_thoth_repo_init import thoth_repo_init_exceptions, thoth_repo_init_in_progress, thoth_repo_init_success
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@register_handler(thoth_repo_init_message.topic_name, ["v1"])
@count_exceptions(thoth_repo_init_exceptions)
@track_inprogress(thoth_repo_init_in_progress)
async def parse_thoth_repo_init_message(repo_init: Dict[str, Any], openshift: OpenShift, **kwargs) -> None:
    """Parse thoth_repo_init message."""
    await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_BACKEND_NAMESPACE)
    workflow_name = openshift.schedule_thoth_repo_init(project_url=repo_init["project_url"])
    _LOGGER.debug(f"Scheduled kebechet workflow {workflow_name}")
    thoth_repo_init_success.inc()
