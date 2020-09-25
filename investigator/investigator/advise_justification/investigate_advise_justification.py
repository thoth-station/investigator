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

"""Expose metrics about advise justification."""

import logging
import os

from .metrics_advise_justification import advise_justification_exceptions
from .metrics_advise_justification import advise_justification_success
from .metrics_advise_justification import advise_justification_in_progress
from .metrics_advise_justification import advise_justification_type_number

_LOGGER = logging.getLogger(__name__)

DEPLOYMENT_NAME = os.environ["THOTH_DEPLOYMENT_NAME"]


@advise_justification_exceptions.count_exceptions()
@advise_justification_in_progress.track_inprogress()
async def expose_advise_justification_metrics(advise_justification):
    """Retrieve adviser reports justifications."""
    advise_justification_type_number.labels(
        advise_message=advise_justification.message,
        justification_type=advise_justification.justification_type,
        thoth_environment=DEPLOYMENT_NAME,
    ).inc(advise_justification.count)
    _LOGGER.info(
        "advise_justification_type_number(%r, %r)=%r",
        advise_justification.message,
        advise_justification.justification_type,
        advise_justification.count,
    )

    advise_justification_success.inc()
