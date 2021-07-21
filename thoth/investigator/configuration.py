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
import json
from enum import Enum, auto
from typing import Union

_LOGGER = logging.getLogger(__name__)


class ConsumerModeEnum(Enum):
    """Class representing the different modes the consumer can use which correspond to different handler tables."""

    investigator = auto()
    metrics = auto()


def _get_ack_on_fail() -> Union[bool, list]:
    to_ret = json.loads(os.getenv("THOTH_INVESTIGATOR_ACK_ON_FAIL", "0"))
    if type(to_ret) == int:
        return bool(to_ret)
    elif type(to_ret) == list:
        return to_ret
    else:
        raise TypeError("THOTH_INVESTIGATOR_ACK_ON_FAIL envvar must be either a integer or a list")


class Configuration:
    """Configuration of investigator."""

    # Namespaces
    THOTH_BACKEND_NAMESPACE = os.environ["THOTH_BACKEND_NAMESPACE"]
    THOTH_MIDDLETIER_NAMESPACE = os.environ["THOTH_MIDDLETIER_NAMESPACE"]

    DEPLOYMENT_NAME = os.environ["THOTH_DEPLOYMENT_NAME"]

    # Workflows
    THOTH_INVESTIGATOR_SCHEDULE_SOLVER = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_SOLVER", 1))
    THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER", 1))
    THOTH_INVESTIGATOR_SCHEDULE_SECURITY = int(os.getenv("THOTH_INVESTIGATOR_SCHEDULE_SECURITY", 1))
    THOTH_INVESTIGATOR_SCHEDULE_KEBECHET_ADMIN = int(os.getenv("THOTH_INVESTIGATOR_KEBECHET_ADMINISTRATOR", 1))

    LOG_SOLVER = os.environ.get("THOTH_LOG_SOLVER") == "DEBUG"
    LOG_REVSOLVER = os.environ.get("THOTH_LOG_REVSOLVER") == "DEBUG"

    # Quota handling
    SLEEP_TIME = int(os.getenv("ARGO_PENDING_SLEEP_TIME", 2))
    PENDING_WORKFLOW_LIMIT = os.getenv("ARGO_PENDING_WORKFLOW_LIMIT", None)

    # Consumer configuration
    MAX_RETRIES = int(os.getenv("THOTH_INVESTIGATOR_MAX_RETRIES", 5))
    BACKOFF = float(os.getenv("THOTH_INVESTIGATOR_BACKOFF", 0.5))  # Linear backoff strategy
    ACK_ON_FAIL = _get_ack_on_fail()
    NUM_WORKERS = int(os.getenv("THOTH_CONSUMER_WORKERS", 5))
    CONSUMER_MODE = os.getenv("THOTH_CONSUMER_MODE", "investigator")
