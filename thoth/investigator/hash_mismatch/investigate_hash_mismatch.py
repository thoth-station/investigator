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

"""Logic for handling hash_mismatch message."""

import asyncio
import logging
from typing import Dict, Any

from ..common import send_advise_request_for_installation, learn_using_solver, register_handler
from ..configuration import Configuration
from ..metrics import scheduled_workflows
from ..github_service import GithubService

from .metrics_hash_mismatch import (
    hash_mismatch_exceptions,
    hash_mismatch_success,
    hash_mismatch_in_progress,
    hash_mismatch_sent_advise_requests,
)
from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import hash_mismatch_message
from thoth.common import OpenShift
from thoth.common.enums import InternalTriggerEnum
from thoth.storages import GraphDatabase

_LOGGER = logging.getLogger(__name__)


@register_handler(hash_mismatch_message.topic_name, ["v1"])
@count_exceptions(hash_mismatch_exceptions)
@track_inprogress(hash_mismatch_in_progress)
async def parse_hash_mismatch(
    mismatch: Dict[str, Any], openshift: OpenShift, graph: GraphDatabase, gh_service: GithubService, **kwargs
):
    """Process a hash mismatch message from package-update producer."""
    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER:
        # Solver logic
        solver_wf_scheduled = await learn_using_solver(
            openshift=openshift,
            graph=graph,
            is_present=False,
            package_name=mismatch["package_name"],
            index_url=mismatch["index_url"],
            package_version=mismatch["package_version"],
        )

        scheduled_workflows.labels(message_type=hash_mismatch_message.base_name, workflow_type="solver").inc(
            solver_wf_scheduled
        )

    if mismatch["missing_from_source"] != []:
        for h in mismatch["missing_from_source"]:
            graph.update_python_package_hash_present_flag(
                package_name=mismatch["package_name"],
                package_version=mismatch["package_version"],
                index_url=mismatch["index_url"],
                sha256_hash=h,
            )

    if Configuration.THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN:
        installations = graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name=mismatch["package_name"],
            package_version=mismatch["package_version"],
            index_url=mismatch["index_url"],
        )
        keb_meta = {
            "message_justification": InternalTriggerEnum.HASH_MISMATCH.value,
            "package_name": mismatch["package_name"],
            "package_version": mismatch["package_version"],
            "package_index": mismatch["index_url"],
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
        hash_mismatch_sent_advise_requests.inc(num_requests_sent)

    hash_mismatch_success.inc()
