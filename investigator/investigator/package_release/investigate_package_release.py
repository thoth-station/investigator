#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Bissenbay Dauletbayev
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

"""This file contains methods used by Thoth investigator to investigate on package releases."""

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.messaging import PackageReleaseMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from .. import common
from .metrics_package_release import package_release_exceptions
from .metrics_package_release import package_release_in_progress
from .metrics_package_release import package_release_success


@package_release_exceptions.count_exceptions()
@package_release_in_progress.track_inprogress()
def parse_package_release_message(package_release: MessageBase, openshift: OpenShift, graph: GraphDatabase) -> None:
    """Parse package release message."""
    package_name = package_release.package_name
    package_version = package_release.package_version
    index_url = package_release.index_url

    common.learn_using_solver(
        openshift=openshift,
        graph=graph,
        is_present=False,
        package_name=package_name,
        index_url=index_url,
        package_version=package_version,
    )

    scheduled_workflows.labels(message_type=PackageReleaseMessage.topic_name, workflow_type="solver").inc()

    package_release_success.inc()
