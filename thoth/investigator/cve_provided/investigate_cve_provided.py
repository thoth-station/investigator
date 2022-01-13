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

import asyncio
import logging
from typing import Dict, Any

from ..common import register_handler, send_advise_request_for_installation
from ..configuration import Configuration
from ..github_service import GithubService

from .metrics_cve_provided import (
    cve_provided_exceptions,
    cve_provided_success,
    cve_provided_in_progress,
    cve_provided_sent_advise_requests,
)
from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import cve_provided_message
from thoth.common import OpenShift
from thoth.storages import GraphDatabase
from thoth.common.enums import InternalTriggerEnum

_LOGGER = logging.getLogger(__name__)


@register_handler(cve_provided_message.topic_name, ["v1"])
@count_exceptions(cve_provided_exceptions)
@track_inprogress(cve_provided_in_progress)
async def parse_cve_provided(
    cve_provided: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, gh_service: GithubService, **kwargs
):
    """Process a cve provided message."""
    # Add more logic if neccessary.

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        installations = graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name=cve_provided["package_name"],
            package_version=cve_provided["package_version"],
            index_url=cve_provided["index_url"],
        )
        keb_meta = {
            "message_justification": InternalTriggerEnum.CVE.value,
            "package_name": cve_provided["package_name"],
            "package_version": cve_provided["package_version"],
            "package_index": cve_provided["index_url"],
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
        cve_provided_sent_advise_requests.inc(num_requests_sent)

    cve_provided_success.inc()
