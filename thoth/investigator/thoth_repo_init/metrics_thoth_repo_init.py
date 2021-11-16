#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2021 Kevin Postlethwait
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

"""Set labels for thoth_repo_init metrics."""

from ..metrics import in_progress, success, exceptions

thoth_repo_init_in_progress = in_progress.labels(message_type="thoth_repo_init")
thoth_repo_init_success = success.labels(message_type="thoth_repo_init")
thoth_repo_init_exceptions = exceptions.labels(message_type="thoth_repo_init")
