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

import logging
from typing import Dict, Callable

from ..common import wait_for_limit, git_source_from_url, register_handler
from ..configuration import Configuration
from .metrics_hash_mismatch import hash_mismatch_exceptions
from .metrics_hash_mismatch import hash_mismatch_success
from .metrics_hash_mismatch import hash_mismatch_in_progress

_LOGGER = logging.getLogger(__name__)

handler_table = {}  # type: Dict[str, Callable]


@register_handler(handler_table, ["v1"])
@hash_mismatch_exceptions.count_exceptions()
@hash_mismatch_in_progress.track_inprogress()
async def parse_hash_mismatch(mismatch, openshift, graph):
    """Process a hash mismatch message from package-update producer."""
    try:
        await wait_for_limit(openshift, workflow_namespace=Configuration.THOTH_MIDDLETIER_NAMESPACE)
        openshift.schedule_all_solvers(
            packages=f"{mismatch.package_name}==={mismatch.package_version}", indexes=[mismatch.index_url],
        )
    except Exception:
        # If we get some errors from OpenShift master - do not retry. Rather schedule the remaining
        # ones and try to schedule the given package in the next run.
        _LOGGER.exception(
            f"Failed to schedule new solver to solve package {mismatch.package_name} in version"
            f" {mismatch.package_version}, the graph refresh job will not fail but will try to reschedule"
            " this in next run",
        )

    if mismatch.missing_from_source != []:
        for h in mismatch.missing_from_source:
            graph.update_python_package_hash_present_flag(
                package_name=mismatch.package_name,
                package_version=mismatch.package_version,
                index_url=mismatch.index_url,
                sha256=h,
            )

    repositories = graph.get_adviser_run_origins_all(
        index_url=mismatch.index_url,
        package_name=mismatch.package_name,
        package_version=mismatch.package_version,
        count=None,
        distinct=True,
    )

    issue_title = f"Hash mismatch for {mismatch.package_name}=={mismatch.package_version} on {mismatch.index_url}"

    def issue_body():
        return "Automated message from package change detected by thoth.package-update"

    for repo in repositories:
        gitservice_repo = git_source_from_url(repo)
        gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)

    hash_mismatch_success.inc()
