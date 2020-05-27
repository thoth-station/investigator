#!/usr/bin/env python3
# thoth-unresolved-package-handler-consumer
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

"""Consume messages to schedule solver with priority."""

import logging
import os

from thoth.messaging import MessageBase, UnresolvedPackageMessage
from thoth.unresolved_package_handler.unresolved_package_handler import send_metrics_to_pushgateway
from thoth.unresolved_package_handler.unresolved_package_handler import parse_unresolved_package_message

DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger("thoth.unresolved_package_handler")

app = MessageBase.app
unresolved_package_message_topic = UnresolvedPackageMessage().topic


@app.agent(unresolved_package_message_topic)
async def consume_unresolved_package(unresolved_packages) -> None:
    """Loop when an unresolved package message is received."""
    async for unresolved_package in unresolved_packages:
        parse_unresolved_package_message(unresolved_package=unresolved_package)


if __name__ == "__main__":
    app.main()
