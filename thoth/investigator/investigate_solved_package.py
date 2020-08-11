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


import sys
import logging
import json
import os

from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

from thoth.storages.graph import GraphDatabase
from thoth.messaging import MessageBase
from thoth.messaging import SolvedPackageMessage
from thoth.common import OpenShift

from thoth.investigator import metrics
from thoth.investigator import common


@metrics.exceptions.count_exceptions()
@metrics.in_progress.track_inprogress()
def parse_solved_package_message(solved_package: MessageBase) -> None:
    """Parse soolved package message."""
    package_name = solved_package.package_name
    package_version = solved_package.package_version
    index_url: str = solved_package.index_url
    solver: str = solved_package.solver

    openshift = OpenShift()

    total_si_wfs_scheduled = 0

    graph = GraphDatabase()
    graph.connect()

    # Adviser logic

    # 1. Retrieve adviser ids for specific thoth_integrations with need_re_run == True

    # 2. For each adviser ids retrieved:
    # check if there are adviser ids with adviser_re_run_ids == adviser_id retrieved
    # if yes do nothing (new adviser runs exist for adviser_id), else:

    # 3. Check if the adviser run has unsolved packages corresponding to the solved one
    # If yes, Schedule adviser workflow with adviser_re_run_id == adviser_id

    # Check if package version index exists in Thoth Knowledge Graph
    is_present = graph.python_package_version_exists(
        package_name=package_name, package_version=version, index_url=index_url
    )

    # SI logic

    si_wfs_scheduled = common.learn_about_security(
        openshift=openshift,
        graph=graph,
        is_present=is_present,
        package_name=package_name,
        package_version=version,
        index_url=index_url,
    )

    metrics.investigator_scheduled_workflows.labels(
        message_type=SolvedPackageMessage.topic_name, workflow_type="security-indicator"
    ).set(si_wfs_scheduled)

    metrics.success.inc()


def _schedule_security_indicator(package_name: str, package_version: str, index_url: str) -> int:
    """Schedule Security Indicator."""
    openshift = OpenShift()
    try:
        analysis_id = openshift.schedule_security_indicator(
            python_package_name=package_name,
            python_package_version=package_version,
            python_package_index=index_url,
            aggregation_function="process_data",
        )
        _LOGGER.info(
            "Scheduled SI %r for package %r in version %r from index %r, analysis is %r",
            package_name,
            package_version,
            index_url,
            analysis_id,
        )
        is_scheduled = 1
    except Exception:
        _LOGGER.warning(
            f"Failed to schedule SI for package {package_name} in version {package_version} from index {index_url}"
        )
        is_scheduled = 0

    return is_scheduled
