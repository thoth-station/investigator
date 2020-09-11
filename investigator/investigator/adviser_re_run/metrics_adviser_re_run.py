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

"""Set labels for adviser re run metrics."""

from ..metrics import in_progress, success, exceptions

adviser_re_run_in_progress = in_progress.labels(message_type="adviser_re_run")
adviser_re_run_success = success.labels(message_type="adviser_re_run")
adviser_re_run_exceptions = exceptions.labels(message_type="adviser_re_run")
