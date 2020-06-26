#!/usr/bin/env python3
# thoth-unresolved-package-handler
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

"""Test unresolved package handler."""

import pytest

from pathlib import Path

from thoth.unresolved_package_handler.unresolved_package_handler import unresolved_package_handler
from thoth.unresolved_package_handler.unresolved_package_handler import parse_unresolved_package_message


class TestProducer:
    """Test producer of unresolved package handler."""

    def test_unresolved_package_handler(self) -> None:
        """Test extraction of inputs for Kafka."""
        file_test_path = Path().cwd().joinpath("tests", "adviser-04ab56d6.json")
        unresolved_packages, solver = unresolved_package_handler(file_test_path=file_test_path)
        unresolved_package = unresolved_packages["black"]
        assert unresolved_package.name == "black"
        assert unresolved_package.version is "*"
        assert unresolved_package.index is None
        assert solver == "solver-rhel-8-py36"
