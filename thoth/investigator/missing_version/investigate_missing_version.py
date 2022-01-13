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

import asyncio
import logging
from typing import Dict, Any

from ..common import send_advise_request_for_installation, register_handler
from ..github_service import GithubService

from .metrics_missing_version import (
    missing_version_exceptions,
    missing_version_in_progress,
    missing_version_success,
    missing_version_sent_advise_requests,
)

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import missing_version_message
from thoth.common import OpenShift
from thoth.common.enums import InternalTriggerEnum
from thoth.storages import GraphDatabase
from ..configuration import Configuration

_LOGGER = logging.getLogger(__name__)


@register_handler(missing_version_message.topic_name, ["v1"])
@count_exceptions(missing_version_exceptions)
@track_inprogress(missing_version_in_progress)
async def parse_missing_version(
    version: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, gh_service: GithubService, **kwargs
):
    """Process a missing version message from package-update producer."""
    graph.update_missing_flag_package_version(
        index_url=version["index_url"],
        package_name=version["package_name"],
        package_version=version["package_version"],
        value=True,
    )
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        installations = graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name=version["package_name"],
            package_version=version["package_version"],
            index_url=version["index_url"],
        )
        keb_meta = {
            "message_justification": InternalTriggerEnum.MISSING_VERSION.value,
            "package_name": version["package_name"],
            "package_version": version["package_version"],
            "package_index": version["index_url"],
        }
        tasks = []
        for key in installations:
            tasks.append(
                send_advise_request_for_installation(
                    slug=key,
                    environment_name=installations[key]["environment_name"],
                    keb_meta=keb_meta,
                    gh_service=gh_service,
                )
            )
        num_requests_sent = sum(await asyncio.gather(*tasks))
        missing_version_sent_advise_requests.inc(num_requests_sent)

    missing_version_success.inc()
