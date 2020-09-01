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


"""This is Thoth investigator."""

from thoth.common import __version__ as __common__version__
from thoth.common import init_logging

from thoth.messaging import __version__ as __messaging__version__
from thoth.storages import __version__ as __storages__version__
from thoth.python import __version__ as __python__version__

from .missing_package import parse_missing_package
from .missing_version import parse_missing_version
from .hash_mismatch import parse_hash_mismatch
from .unresolved_package import parse_unresolved_package_message
from .unrevsolved_package import parse_revsolved_package_message
from .solved_package import parse_solved_package_message

__version__ = "0.4.2"
__service_version__ = (
    f"{__version__}+"
    f"messaging.{__messaging__version__}.storages.{__storages__version__}."
    f"common.{__common__version__}.python.{__python__version__}"
)

# Init logging here when gunicorn import this application.
init_logging()

__all__ = [
    "parse_missing_package",
    "parse_missing_version",
    "parse_hash_mismatch",
    "parse_unresolved_package_message",
    "parse_revsolved_package_message",
    "parse_solved_package_message",
]
