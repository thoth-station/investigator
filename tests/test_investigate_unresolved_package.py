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

from .base_test import InvestigatorTestCase
from thoth.investigator.investigate_unresolved_package import investigate_unresolved_package


class TestProducer(InvestigatorTestCase):
    """Test producer of unresolved package handler."""

    _ADVISER_DOCUMENT_PATH = InvestigatorTestCase.DATA / "adviser-04ab56d6.json"

    def test_investigate_unresolved_package(self) -> None:
        """Test extraction of inputs for Kafka."""
        unresolved_packages, solver = investigate_unresolved_package(file_test_path=self._ADVISER_DOCUMENT_PATH)
        unresolved_package = unresolved_packages["black"]
        assert unresolved_package.name == "black"
        assert unresolved_package.version is "*"
        assert unresolved_package.index is None
        assert solver == "solver-rhel-8-py36"
