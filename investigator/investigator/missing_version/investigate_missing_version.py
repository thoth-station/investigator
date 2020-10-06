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

import logging

from ..common import git_source_from_url, schedule_kebechet_run_url
from ..metrics import scheduled_workflows

from .metrics_missing_version import missing_version_exceptions
from .metrics_missing_version import missing_version_in_progress
from .metrics_missing_version import missing_version_success

from prometheus_async.aio import track_inprogress, count_exceptions
from thoth.messaging import MissingVersionMessage

_LOGGER = logging.getLogger(__name__)


@count_exceptions(missing_version_exceptions)
@track_inprogress(missing_version_in_progress)
async def parse_missing_version(version, openshift, graph):
    """Process a missing version message from package-update producer."""
    graph.update_missing_flag_package_version(
        index_url=version.index_url,
        package_name=version.package_name,
        package_version=version.package_version,
        value=True,
    )

    repositories = graph.get_adviser_run_origins_all(
        index_url=version.index_url,
        package_name=version.package_name,
        package_version=version.package_version,
        count=None,
        distinct=True,
    )

    issue_title = f"Missing package version {version.package_name}=={version.package_version} on {version.index_url}"

    def issue_body():
        return "Automated message from package change detected by thoth.package-update"

    kebechet_wf_scheduled = 0

    for repo in repositories:
        gitservice_repo = git_source_from_url(repo)

        is_scheduled = schedule_kebechet_run_url(repo=repo, gitservice_repo_name=gitservice_repo.service_type.name)
        kebechet_wf_scheduled += is_scheduled

        gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)

    scheduled_workflows.labels(message_type=MissingVersionMessage.topic_name, workflow_type="kebechet").inc(
        kebechet_wf_scheduled
    )

    missing_version_success.inc()
