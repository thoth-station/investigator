#!/usr/bin/env python3
# thoth-investigator-consumer
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


"""Consume messages to schedule workflows to learn something about a package."""


import logging
import os
import asyncio
import json
import signal
from runpy import run_module
from aiohttp import web
from time import sleep

from typing import Optional

import thoth.messaging.consumer as consumer
import thoth.messaging.admin_client as admin
from thoth.messaging import ALL_MESSAGES

from thoth.investigator import __service_version__
from thoth.investigator.configuration import Configuration
from thoth.investigator.common import handler_table
from thoth.investigator.metrics import registry, failures, subscribed_topics

from thoth.common import OpenShift, init_logging
from thoth.storages.graph import GraphDatabase

from prometheus_client import generate_latest
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Consumer

# We run all the modules so that their metrics and handlers get registered
run_module("thoth.investigator.advise_justification.investigate_advise_justification")
run_module("thoth.investigator.adviser_re_run.investigate_adviser_re_run")
run_module("thoth.investigator.adviser_trigger.investigate_adviser_trigger")
run_module("thoth.investigator.cve_provided.investigate_cve_provided")
run_module("thoth.investigator.hash_mismatch.investigate_hash_mismatch")
run_module("thoth.investigator.kebechet_run_url_trigger.investigate_kebechet_run_url_trigger")
run_module("thoth.investigator.kebechet_trigger.investigate_kebechet_trigger")
run_module("thoth.investigator.missing_package.investigate_missing_package")
run_module("thoth.investigator.missing_version.investigate_missing_version")
run_module("thoth.investigator.package_extract_trigger.investigate_package_extract_trigger")
run_module("thoth.investigator.package_released.investigate_package_released")
run_module("thoth.investigator.provenance_checker_trigger.investigate_provenance_checker_trigger")
run_module("thoth.investigator.qebhwt_trigger.investigate_qebhwt_trigger")
run_module("thoth.investigator.si_unanalyzed_package.investigate_si_unanalyzed_package")
run_module("thoth.investigator.solved_package.investigate_solved_package")
run_module("thoth.investigator.unresolved_package.investigate_unresolved_package")
run_module("thoth.investigator.unrevsolved_package.investigate_unrevsolved_package")
run_module("thoth.investigator.update_provide_source_distro.investigate_update_provide_source_distro")

init_logging()

# set up logging
DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 0)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Thoth Investigator consumer v%s", __service_version__)

# Conditional scheduling, by default we schedule everything.
_LOGGER.info("Schedule Solver Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_SOLVER)
_LOGGER.info("Schedule Reverse Solver Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_REVSOLVER)
_LOGGER.info("Schedule Unanalyzed SI Messages set to - %r", Configuration.THOTH_INVESTIGATOR_SCHEDULE_SECURITY)

openshift = OpenShift()
graph = GraphDatabase()

graph.connect()

running = True

routes = web.RouteTableDef()

c = None  # type: Optional[Consumer]


def _handler_lookup(topic_name, version):
    return handler_table[topic_name][version]


def _get_class_from_topic_name(topic_name):
    for i in ALL_MESSAGES:
        if i().topic_name == topic_name:
            return i


def _get_class_from_base_name(base_name):
    for i in ALL_MESSAGES:
        if i.base_name == base_name:
            return i


@routes.get("/metrics")
async def get_metrics(request):
    """Display prometheus metrics."""
    return web.Response(text=generate_latest(registry=registry).decode("utf-8"))


@routes.get("/_health")
async def get_health(request):
    """Display readiness probe."""
    data = {"status": "ready", "version": __service_version__}
    return web.json_response(data)


@routes.get("/subscribe/{base_topic_name}")
async def sub_to_topic(request, base_topic_name):
    """Subscribe to a topic, this function prepends thoth-deployment-name to any topic passed."""
    global c
    message_class = _get_class_from_base_name(base_topic_name)
    if c is None:
        _LOGGER.debug("Consumer has not been created yet, cannot subscribe to topic.")
    if message_class:
        consumer.subscribe_to_message(c, message_class)
        subscribed_topics.labels(base_topic_name).set(1)
        data = {"message": f"Successfully subscribed to {message_class().topic_name}."}
    else:
        # THIS COULD BE REPLACED WITH SOME ERROR CODE INSTEAD
        prefix = os.getenv("THOTH_DEPLOYMENT_NAME", None)
        topic = base_topic_name
        if prefix:
            topic = f"{prefix}.{topic}"
        c.subscribe([topic])
        subscribed_topics.labels(base_topic_name).set(1)
        data = {"message": f"No corresponding message type found in `thoth-messaging`. Subscribed to {topic} instead."}

    return web.json_response(data)


async def _worker(q: asyncio.Queue):
    global c
    if c is None:
        raise Exception
    while True:
        val = await q.get()
        if val is None:
            break
        func, msg = val
        contents = json.loads(msg.value().decode("utf-8"))
        for i in range(0, Configuration.MAX_RETRIES):
            try:
                await func(contents, openshift=openshift, graph=graph)
                c.commit(message=msg)
            except Exception as e:
                _LOGGER.warn(e)
                await asyncio.sleep(Configuration.BACKOFF * i)  # linear backoff strategy
        else:
            # message has exceeded maximum number of retries
            # FAILURE logic
            message_class = _get_class_from_topic_name(msg.topic())
            if Configuration.ACK_ON_FAIL:
                message_type = message_class.base_name.rsplit(".", maxsplit=1)[-1]  # type: str
                message_type = message_type.replace("-", "_")  # this is to match the metrics associate with processing
                failures.labels(message_type=message_type).inc()
                c.commit(message=msg)
            else:
                # unsubscribe from topic
                c.unsubscribe(msg.topic())
                subscribed_topics.labels(base_topic_name=message_class.base_name).set(
                    0
                )  # TODO: add alert trigger when message is unsubscribed from
        await asyncio.sleep(0)  # allow another coroutine to take control


# this consumers from Kafka, but produces to async queue
async def _confluent_consumer_loop(q: asyncio.Queue):
    global c
    if c is None:
        raise Exception
    await asyncio.sleep(1.0)  # wait here so that kafka has time to finish creating topics
    try:
        consumer.subscribe_to_all(c)
        while running:
            msg = c.poll(0)
            if msg is None:
                await asyncio.sleep(1.0)
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    _LOGGER.warning("%s [%d] reached end at offset %d", msg.topic(), msg.partition(), msg.offset())
                else:
                    raise KafkaException(msg.error())
            else:
                contents = json.loads(msg.value().decode("utf-8"))  # type: dict
                v = contents.get("version", "v1")
                func = _handler_lookup(msg.topic(), v)
                await q.put((func, msg))
            await asyncio.sleep(0)
    finally:
        c.close()
        for _ in range(Configuration.NUM_WORKERS):
            await q.put(None)  # each worker can receive this value exactly once


async def _shutdown(app, bar):
    global running
    running = False


if __name__ == "__main__":
    a = admin.create_admin_client()
    admin.create_all_topics(a)
    sleep(1.0)
    loop = asyncio.get_event_loop()
    c = consumer.create_consumer()
    queue = asyncio.Queue(maxsize=10, loop=loop)  # type: asyncio.Queue

    tasks = []
    tasks.append(_confluent_consumer_loop(q=queue))
    for _ in range(Configuration.NUM_WORKERS):
        tasks.append(_worker(q=queue))

    signal.signal(signal.SIGINT, _shutdown)

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app, handle_signals=True)
    loop.run_until_complete(runner.setup())

    site = web.TCPSite(runner, port=6066)
    tasks.append(site.start())

    loop.run_until_complete(asyncio.gather(*tasks))
