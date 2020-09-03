#!/usr/bin/env python3
# thoth-investigator
# Copyright(C) 2020 Christoph Görn
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


"""This is Thoth investigator consumer metrics."""


from . import __service_version__

from prometheus_client import Gauge, Counter


# add the application version info metric
investigator_info = Gauge("investigator_consumer_info", "Investigator Version Info", labelnames=["version"])
investigator_info.labels(version=__service_version__).inc()

# Metrics for Kafka
in_progress = Gauge("investigators_in_progress", "Total number of investigation messages currently being processed.")
exceptions = Counter("investigator_exceptions", "Number of investigation messages which failed to be processed.")
success = Counter("investigators_processed", "Number of investigation messages which were successfully processed.")

# Scheduled workflows
investigator_scheduled_workflows = Gauge(
    "thoth_investigator_scheduled_workflows",
    "Scheduled workflows by investigator per type.",
    ["message_type", "workflow_type"],
)
