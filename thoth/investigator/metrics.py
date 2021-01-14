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

from prometheus_client import Gauge, Counter, CollectorRegistry

registry = CollectorRegistry()

# add the application version info metric
investigator_info = Gauge(
    "thoth_investigator_consumer_info", "Investigator Version Info", labelnames=["version"], registry=registry,
)
investigator_info.labels(version=__service_version__).inc()

# Metrics for Kafka
in_progress = Gauge(
    "thoth_investigator_in_progress",
    "Total number of investigation messages currently being processed.",
    labelnames=["message_type"],
    registry=registry,
)
exceptions = Counter(
    "thoth_investigator_exceptions",
    "Number of investigation messages which failed to be processed.",
    labelnames=["message_type"],
    registry=registry,
)
success = Counter(
    "thoth_investigator_processed",
    "Number of investigation messages which were successfully processed.",
    labelnames=["message_type"],
    registry=registry,
)

failures = Counter(
    "thoth_investigator_failures",
    "Incremented when retry limit for message processing is exceeded.",
    labelnames=["message_type"],
    registry=registry,
)

# Scheduled workflows
scheduled_workflows = Counter(
    "thoth_investigator_scheduled_workflows",
    "Scheduled workflows by investigator per type.",
    ["message_type", "workflow_type"],
    registry=registry,
)

paused_topics = Gauge(
    "thoth_investigator_paused_topics",
    "Boolean gauge indicating whether consumption of the topic has been paused.",
    labelnames=["base_topic_name"],
    registry=registry,
)
