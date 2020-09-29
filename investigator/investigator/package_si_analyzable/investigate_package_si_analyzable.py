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

"""Investigate about SI analyzable packages."""

import logging
import os

from .metrics_package_si_analyzable import package_si_analyzable_exceptions
from .metrics_package_si_analyzable import package_si_analyzable_success
from .metrics_package_si_analyzable import package_si_analyzable_in_progress

_LOGGER = logging.getLogger(__name__)


@package_si_analyzable_exceptions.count_exceptions()
@package_si_analyzable_in_progress.track_inprogress()
async def parse_package_si_analyzable_message(package_si_analyzable, graph):
    """Parse SI analyzable package message."""
    graph.update_is_si_analyzable_flag_package_version(
        package_name=package_si_analyzable.package_name,
        package_version=package_si_analyzable.package_version,
        index_url=package_si_analyzable.index_url,
        value=package_si_analyzable.value
    )

    _LOGGER.info(
        "package %r version %r from %r is SI analyzable? %r",
        package_si_analyzable.package_name,
        package_si_analyzable.package_version,
        package_si_analyzable.index_url,
        package_si_analyzable.value
    )

    package_si_analyzable_success.inc()
