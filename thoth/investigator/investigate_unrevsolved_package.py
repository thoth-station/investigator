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


"""This file contains methods used by Thoth investigator to investigate on unrevsolved packages."""


import logging

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.messaging import UnrevsolvedPackageMessage
from thoth.common import OpenShift

from thoth.investigator import metrics
from thoth.investigator import common

_LOGGER = logging.getLogger(__name__)


@metrics.exceptions.count_exceptions()
@metrics.in_progress.track_inprogress()
def parse_revsolved_package_message(unrevsolved_package: MessageBase, openshift: OpenShift) -> None:
    """Parse soolved package message."""
    package_name = unrevsolved_package.package_name
    package_version = unrevsolved_package.package_version

    # Revsolver logic

    revsolver_wfs_scheduled, revsolver_packages_seen = common.learn_using_revsolver(
        openshift=openshift,
        is_present=is_present,
        package_name=package_name,
        package_version=version,
        revsolver_packages_seen=[],
    )

    metrics.investigator_scheduled_workflows.labels(
        message_type=UnrevsolvedPackageMessage.topic_name, workflow_type="revsolver"
    ).set(revsolver_wfs_scheduled)

    metrics.success.inc()
