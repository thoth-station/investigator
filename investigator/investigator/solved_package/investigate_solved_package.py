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

import logging

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.messaging import SolvedPackageMessage
from thoth.common import OpenShift

from ..metrics import scheduled_workflows
from .. import common

from .metrics_solved_package import solved_package_exceptions
from .metrics_solved_package import solved_package_success
from .metrics_solved_package import solved_package_in_progress

_LOGGER = logging.getLogger(__name__)


@solved_package_exceptions.count_exceptions()
@solved_package_in_progress.track_inprogress()
def parse_solved_package_message(solved_package: MessageBase, openshift: OpenShift, graph: GraphDatabase) -> None:
    """Parse solved package message."""
    package_name = solved_package.package_name
    package_version = solved_package.package_version
    index_url: str = solved_package.index_url

    # SI logic

    si_wfs_scheduled = common.learn_about_security(
        openshift=openshift,
        graph=graph,
        is_present=True,
        package_name=package_name,
        package_version=package_version,
        index_url=index_url,
    )

    scheduled_workflows.labels(message_type=SolvedPackageMessage.topic_name, workflow_type="security-indicator").set(
        si_wfs_scheduled
    )

    solved_package_success.inc()
