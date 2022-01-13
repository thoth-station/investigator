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

"""This file contains methods used by Thoth investigator to investigate on solved packages."""

import asyncio
import logging
import semver
from typing import Dict, Any

from thoth.storages.graph import GraphDatabase
from thoth.messaging import solved_package_message
from thoth.common import OpenShift
from thoth.common.enums import InternalTriggerEnum

from ..metrics import scheduled_workflows
from .. import common
from ..configuration import Configuration
from ..common import register_handler, send_advise_request_for_installation
from ..github_service import GithubService

from .metrics_solved_package import solved_package_exceptions
from .metrics_solved_package import solved_package_success
from .metrics_solved_package import solved_package_in_progress
from .metrics_solved_package import solved_package_sent_advise_requests
from prometheus_async.aio import count_exceptions, track_inprogress

_LOGGER = logging.getLogger(__name__)


@register_handler(solved_package_message.topic_name, ["v1"])
@count_exceptions(solved_package_exceptions)
@track_inprogress(solved_package_in_progress)
async def parse_solved_package_message(
    solved_package: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, gh_service: GithubService, **kwargs
) -> None:
    """Parse solved package message."""
    package_name = solved_package["package_name"]
    package_version = solved_package["package_version"]
    index_url: str = solved_package["index_url"]

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY:
        # SI logic
        si_wfs_scheduled = await common.learn_about_security(
            openshift=openshift,
            graph=graph,
            is_present=True,
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
        )

        scheduled_workflows.labels(
            message_type=solved_package_message.base_name, workflow_type="security-indicator"
        ).inc(si_wfs_scheduled)

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        solver_dict = OpenShift.parse_python_solver_name(solved_package.get("solver"))
        os_name, os_version, python_version = (
            solver_dict["os_name"],
            solver_dict["os_version"],
            solver_dict["python_version"],
        )
        installations = graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name=package_name,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )
        keb_meta = {
            "message_justification": InternalTriggerEnum.NEW_RELEASE.value,
            "package_name": package_name,
            "package_version": package_version,
            "package_index": index_url,
        }
        tasks = []
        for key in installations:
            if semver.compare(package_version, installations[key]["package_version"]) < 0:  # only request if newer
                tasks.append(
                    send_advise_request_for_installation(
                        slug=key,
                        environment_name=installations[key]["environment_name"],
                        keb_meta=keb_meta,
                        gh_service=gh_service,
                    )
                )
        num_requests_sent = sum(await asyncio.gather(*tasks))
        solved_package_sent_advise_requests.inc(num_requests_sent)

    solved_package_success.inc()
