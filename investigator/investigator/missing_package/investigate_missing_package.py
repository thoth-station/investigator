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

import re

from .metrics_missing_package import missing_package_exceptions
from .metrics_missing_package import missing_package_success
from .metrics_missing_package import missing_package_in_progress
from ..common import git_source_from_url, wait_for_limit


@missing_package_exceptions.count_exceptions()
@missing_package_in_progress.track_inprogress()
async def parse_missing_package(package, openshift, graph):
    """Process a missing package message from package-update producer."""
    repositories = graph.get_adviser_run_origins_all(
        index_url=package.index_url, package_name=package.package_name, count=None, distinct=True,
    )

    issue_title = f"Missing package {package.package_name} on {package.index_url}"

    def issue_body():
        return "Automated message from package change detected by thoth.package-update"

    for repo in repositories:
        gitservice_repo = git_source_from_url(repo)
        requirements = re.split("\n| ", gitservice_repo.service.get_project().get_file_content("Pipfile"))
        if package.package_name in requirements:
            gitservice_repo.open_issue_if_not_exist(issue_title, issue_body)
        else:
            await wait_for_limit(openshift)
            openshift.schedule_kebechet_run_url(repo, gitservice_repo.service_type.name)

    missing_package_success.inc()
