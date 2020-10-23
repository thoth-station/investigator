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

"""Investigate about SI analyzable packages due to missing source distro."""

from typing import Dict, Any
import logging

from thoth.messaging import UpdateProvidesSourceDistroMessage
from thoth.storages import GraphDatabase

from ..common import register_handler

from .metrics_update_provide_source_distro import update_provide_source_distro_exceptions
from .metrics_update_provide_source_distro import update_provide_source_distro_success
from .metrics_update_provide_source_distro import update_provide_source_distro_in_progress
from prometheus_async.aio import track_inprogress, count_exceptions

_LOGGER = logging.getLogger(__name__)


@count_exceptions(update_provide_source_distro_exceptions)
@track_inprogress(update_provide_source_distro_in_progress)
@register_handler(UpdateProvidesSourceDistroMessage().topic_name, ["v1"])
async def parse_update_provide_source_distro_message(
    update_provide_source_distro: Dict[str, Any], graph: GraphDatabase
):
    """Parse update provide source distro message."""
    graph.update_provides_source_distro_package_version(
        package_name=update_provide_source_distro["package_name"],
        package_version=update_provide_source_distro["package_version"],
        index_url=update_provide_source_distro["index_url"],
        value=update_provide_source_distro["value"],
    )

    _LOGGER.info(
        "package %r version %r from %r provides source distro? %r",
        update_provide_source_distro["package_name"],
        update_provide_source_distro["package_version"],
        update_provide_source_distro["index_url"],
        update_provide_source_distro["value"],
    )

    update_provide_source_distro_success.inc()
