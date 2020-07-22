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


from thoth.investigator import __service_version__

from prometheus_client import CollectorRegistry, Gauge, Counter


# A registry for the consumer metrics...
prometheus_registry = CollectorRegistry()

# add the application version info metric
_API_GAUGE_METRIC = Gauge(
    "investigator_consumer_info", "Investigator Version Info", labelnames=["version"], registry=prometheus_registry,
)
_API_GAUGE_METRIC.labels(version=__service_version__).inc()

# Metrics for Kafka
IN_PROGRESS_GAUGE = Gauge(
    "investigators_in_progress",
    "Total number of investigation messages currently being processed.",
    registry=prometheus_registry,
)
EXCEPTIONS_COUNTER = Counter(
    "investigator_exceptions",
    "Number of investigation messages which failed to be processed.",
    registry=prometheus_registry,
)
SUCCESSES_COUNTER = Counter(
    "investigators_processed",
    "Number of investigation messages which were successfully processed.",
    registry=prometheus_registry,
)

# Scheduled workflows
investigator_scheduled_workflows = Gauge(
    "thoth_investigator_scheduled_workflows",
    "Scheduled workflows by investigator per type.",
    ["message_type", "workflow_type"],
)
