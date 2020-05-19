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

from unresolved_package_handler import unresolved_package_handler


class TestProducer:
    """Test producer of unresolved package handler."""

    def test_unresolved_package_handler(self) -> None:
        """Test extraction of inputs for Kafka."""
        file_test_path = Path().cwd().joinpath("tests", "adviser-04ab56d6.json")
        unresolved_packages, package_version, sources, solver = unresolved_package_handler(
            file_test_path=file_test_path
        )
        assert unresolved_packages == ["black"]
        assert package_version is None
        assert sources == ["https://pypi.python.org/simple"]
        assert solver == "solver-rhel-8-py36"
