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

import asyncio
from typing import Dict, Any
import logging

from .metrics_missing_package import missing_package_exceptions
from .metrics_missing_package import missing_package_success
from .metrics_missing_package import missing_package_in_progress
from .metrics_missing_package import missing_package_sent_advise_requests
from ..common import register_handler, Configuration, send_advise_request_for_installation
from ..github_service import GithubService

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import missing_package_message
from thoth.storages import GraphDatabase
from thoth.common import OpenShift
from thoth.common.enums import InternalTriggerEnum

_LOGGER = logging.getLogger(__name__)


@register_handler(missing_package_message.topic_name, ["v1"])
@count_exceptions(missing_package_exceptions)
@track_inprogress(missing_package_in_progress)
async def parse_missing_package(
    package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, gh_service: GithubService, **kwargs
):
    """Process a missing package message from package-update producer."""
    python_package_versions = graph.get_python_package_versions_all(
        package_name=package["package_name"],
        index_url=package["index_url"],
        count=None,
    )

    for _, version, _ in python_package_versions:
        graph.update_missing_flag_package_version(
            package_name=package["package_name"],
            package_version=version,
            index_url=package["index_url"],
            value=True,
        )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        installations = graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name=package["package_name"],
            index_url=package["index_url"],
        )
        keb_meta = {
            "message_justification": InternalTriggerEnum.MISSING_PACKAGE.value,
            "package_name": package["package_name"],
            "package_index": package["index_url"],
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
        missing_package_sent_advise_requests.inc(num_requests_sent)

    missing_package_success.inc()
