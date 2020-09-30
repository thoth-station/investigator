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


"""This is Thoth investigator configuration parameters."""


import logging
import os

_LOGGER = logging.getLogger(__name__)


class Configuration:
    """Configuration of investigator."""

    # Namespaces
    THOTH_BACKEND_NAMESPACE = os.environ["THOTH_BACKEND_NAMESPACE"]
    THOTH_MIDDLETIER_NAMESPACE = os.environ["THOTH_MIDDLETIER_NAMESPACE"]

    # Workflows
    THOTH_INVESTIGATOR_SCHEDULE_SOLVER = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_SOLVER", 1))
    THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER", 1))
    THOTH_INVESTIGATOR_SCHEDULE_SECURITY = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_SECURITY", 1))

    _LOG_SOLVER = os.environ.get("THOTH_LOG_SOLVER") == "DEBUG"
    _LOG_REVSOLVER = os.environ.get("THOTH_LOG_REVSOLVER") == "DEBUG"

    GITHUB_PRIVATE_TOKEN = os.getenv("THOTH_GITHUB_PRIVATE_TOKEN")
    GITLAB_PRIVATE_TOKEN = os.getenv("THOTH_GITLAB_PRIVATE_TOKEN")

    # Quota handling
    SLEEP_TIME = int(os.getenv("ARGO_PENDING_SLEEP_TIME", 2))
    _PENDING_WORKFLOW_LIMIT = os.getenv("ARGO_PENDING_WORKFLOW_LIMIT", None)