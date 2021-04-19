Welcome to Thoth's investigator documentation
---------------------------------------------

Thoth's investigator is a Kafka based component that consumes all messages produced by Thoth components.

It has monitoring system in places that allow Thoth team to see what is happening in Thoth in terms of Kafka, Openshift, Argo for the different components
and act when some alarms are received.

This agent relies mainly on:

* `thoth-messaging <https://github.com/thoth-station/messaging>`__ to handle Kafka messages.

* `thoth-common <https://github.com/thoth-station/common>`__ to schedule Argo workflows.

* `thoth-storages <https://github.com/thoth-station/storages>`__ to set/verify content in database.


This documentation corresponds to a component called "investigator". Sources can be
found on `GitHub <https://github.com/thoth-station/investigator>`_.

See `thoth-station <https://thoth-station.ninja>`_ website and `Thoth-Station
organization on GitHub <https://github.com/thoth-station>`_.

Goals
=====

* Receive messages from different components and take action depending on the info about a package. (Consumer)

Environment variables
=====================

**bold** indicates required, *italicized* indicates optional

See `thoth-messaging <https://github.com/thoth-station/messaging>`__:

* **KAFKA_BOOTSTRAP_SERVERS**: a comma seperated list of Kafka bootstrap servers.
* *KAFKA_SECURITY_PROTOCOL*: specify what security protocol to use.

  * *KAFKA_SSL_CERTIFICATE_LOCATION* (if security protocol is `SSL`).
  * *KAFKA_SASL_USERNAME* and *KAFKA_SASL_PASSWORD* (if security protocol is `SASL`).

* **KAFKA_CONSUMER_GROUP_ID**: specify Kafka consumer group, if two consumers have the same group then message
  partitions are split between them. You can have a number of consumers equal to the number of message partitions.
* *KAFKA_CONSUMER_MAX_POLL_INTERVAL_MS*: This is a timeout, if the consumer does not poll for messages for **N** seconds
  then throws an error, when blocking for workflow limits this should be set moderately high. The default value is `300000`.
* **KAFKA_CONSUMER_ENABLE_AUTOCOMMIT**: This should be set to `False` so that we don't commit messages which have not
  been fully processed yet. Investigator will handle commiting messages.


Git Services:

* `THOTH_GITHUB_PRIVATE_TOKEN`: token for authenticating actions on GitHub repositories

* `THOTH_GITLAB_PRIVATE_TOKEN`: token for authenticating actions on GitLab repositories

Enforcing a workflow limit:

* `ARGO_PENDING_SLEEP_TIME`: amount of time we wait between checking the number of workflows in progress

* `ARGO_PENDING_WORKFLOW_LIMIT`: limit to enforce on argo for total number of pending workflows


Kafka/Argo combination in Project Thoth
========================================

Thoth relies on Kafka and Argo for message handling and Argo workflows for services respectively.

Several types of messages are handled by investigator and different type of actions are performed. In particular we can distinguish
different categories of messages in Thoth as described in the following sections.

Increase Thoth Knowledge
=========================

The following messages are sent by different Thoth components:

* `PackageReleasedMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/package_released/README.md>`__.

* `UnresolvedPackageMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/unresolved_package/README.md>`__.

* `UnrevsolvedPackageMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/unrevsolved_package/README.md>`__.

* `SIUnanalyzedPackageMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/si_unanalyzed_package/README.md>`__.

* `SolvedPackageMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/solved_package/README.md>`__.

* `CVEProvidedMessage <https://github.com/thoth-station/messaging/blob/master/thoth/messaging/cve_provided.py>`__.

Monitor Thoth results and knowledge
===================================

The following message is sent by `advise reporter producer <https://github.com/thoth-station/advise-reporter>`__ to show the use of recomendations across all Thoth integrations:

* `AdviseJustificationMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/advise_justification/README.md>`__.

The following messages are sent by `package update producer <https://github.com/thoth-station/package-update-job>`__ to keep knowledge in the database up to date:

* `HashMismatchMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/hash_mismatch/README.md>`__.

* `MissingPackageMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/missing_package/README.md>`__

* `MissingVersionMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/missing_version/README.md>`__

* `UpdateProvidesSourceDistroMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/update_provide_source_distro/README.md>`__

The following message is sent by `solver <https://github.com/thoth-station/solver>`__ when Thoth acquired all missing knowledge required to provide advice to a user (human or bot):

* `AdviserReRunMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/advise_justification/README.md>`__.

Trigger User requests
=====================

The following messages are sent by `User-API producer <https://github.com/thoth-station/user-api>`__ when users (humans or bots)
interact with `Thoth integrations <https://github.com/thoth-station/adviser/blob/master/docs/source/integration.rst>`__:

* `AdviserTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/adviser_trigger/README.md>`__.

* `KebechetTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/kebechet_trigger/README.md>`__

* `PackageExtractTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/package_extract_trigger/README.md>`__

* `ProvenanceCheckerTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/provenance_checker_trigger/README.md>`__

* `QebHwtTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/qebhwt_trigger/README.md>`__

The following message is triggered internally to keep user repositories fresh when new Thoth knowledge is encountered:

* `KebechetRunUrlTriggerMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/kebechet_run_url_trigger/README.md>`__


Investigator scenarios description
==================================

Thoth knowledge increase using investigator
###########################################

.. image:: https://raw.githubusercontent.com/thoth-station/investigator/master/thoth/investigator/images/IncreaseThothKnowledge.jpg
   :align: center
   :alt: Thoth knowledge increase using investigator.

The image above shows how Thoth keeps learning automatically using two fundamental components that produce messages described in this section:

* `package release producer <https://github.com/thoth-station/package-releases-job>`__ to acquire knowledge on newly released package version from a certain index.

* `graph-refresh producer <https://github.com/thoth-station/graph-refresh-job>`__ to allow Thoth continuosly learn and keep the internal knowledge up to date.

Thoth self-learn on errors during knowledge acquisition
########################################################

.. image:: https://raw.githubusercontent.com/thoth-station/investigator/master/thoth/investigator/images/UpdateProvidesSourceDistro.jpg
   :align: center
   :alt: Thoth self-learn on errors during knowledge acquisition.

The image above shows how Thoth is able to self-learn and act on known errors during knowledge acquisition about Security for a certain package:

* if a package, version from a certain index cannot be downloaded because the source distro is missing or the package is missing SI workflow will send messages
(`UpdateProvidesSourceDistroMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/update_provide_source_distro/README.md>`__ or
`MissingVersionMessage <https://github.com/thoth-station/investigator/blob/master/thoth/investigator/missing_version/README.md>`__ respectively)

* Investigator takes the messages and acts setting flags for those packages in Thoth knowledge graph so that next time Thoth is not going to schedule security analysis
for that package. (In the image below what Grafana dashboard shows)

.. image:: https://raw.githubusercontent.com/thoth-station/investigator/master/thoth/investigator/images/SIAnalysisOverview.png
   :align: center
   :alt: Thoth SI Analysis monitoring.

Thoth self-heal when knowledge is missing in providing an advise
#################################################################

.. image:: https://raw.githubusercontent.com/thoth-station/investigator/master/thoth/investigator/images/FailedAdviceAdviserReRun.jpg
   :align: center
   :alt: Thoth self-heal when knowledge is missing in providing an advise.

The image above shows how Thoth is able to self-heal when knowledge is missing in providing an advise:

* When a user requests Thoth advice, but there is missing information to provide it, the adviser Argo workflow
will send a message to Kafka (`UnresolvedPackageMessage <https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py>`__)
through one of its tasks which depends on `thoth-messaging <https://github.com/thoth-station/messaging>`__ library.

* investigator will consume these event messages and schedule solver workflows accordingly so that Thoth can learn about missing information.

* During solver workflow two Kafka messages are sent out:
  * `SolvedPackageMessage <https://github.com/thoth-station/messaging/blob/master/thoth/messaging/solved_package.py>`__, used by investigator to schedule the next information that needs to be learned by Thoth e.g security information.
  * `AdviserTriggerMessage <https://github.com/thoth-station/messaging/blob/master/thoth/messaging/adviser_trigger.py>`__, that contains all information required by investigator to reschedule an adviser that previously failed.

* The loop is closed once the adviser workflow re-run is successful in providing advice.

This self-learning data-driven pipeline with Argo and Kafka is fundamental for all Thoth integrations because it will make Thoth learn about new packages
and keep its knowledge up to date to what users use in their software stacks.

Users interaction with Thoth services
#####################################

.. image:: https://raw.githubusercontent.com/thoth-station/investigator/master/thoth/investigator/images/UserAPIKafkaProducer.jpg
   :align: center
   :alt: Users interaction with Thoth services.

The image above explains what happen when a User of Thoth (Human or Bot) interacts with one of Thoth integrations.


Dev Guide
=========

Most of the additions to this repository will entail adding new messages to process. That is what is being documented
here, if you feel that any information is missing please feel free to open an issue.

For each message there are two things you should implement:

1. message processing
2. consumer metrics

create a new directory in thoth/investigator which looks like this:

* message_name

  * `__init__.py`
  * investigate_<message_name>.py
  * metrics_<message_name>.py
  * `README.md` describing the message and what happens once consumed by investigator.

Message Parsing
================

The implentation of this portion is highly specific to your own problem so not much can be advised in terms of rules
and regulations. In general calling the function `parse_<message_name>_message` is best practice.  Make sure to include
the three basic metrics to your function:

.. code-block:: python

  @foo_exceptions.count_exceptions()
  @foo_in_progress.track_inprogress()
  def parse_foo_message(message):
      # do stuff
      foo_success.inc()

  # <message_name> = foo


Consumer Metrics
================

For consumer metrics you should at least have the following three:

* <message_name>_exceptions (prometheus Counter)
* <message_name>_success (prometheus Counter)
* <message_name>_in_progress (prometheus Gauge)

These are extensions of the metrics in `thoth/investigator/metrics.py`

The following is an example of a basic metrics file for a message `foo`:

.. code-block:: python

  from ..metrics import in_progress, success, exceptions

  foo_in_progress = in_progress.labels(message_type="foo")
  foo_success = success.labels(message_type="foo")
  foo_exceptions = exceptions.labels(message_type="foo")

You can add metrics as you see fit, but if the metric is not specific only to your messages please move it to
thoth/investigator/metrics.py and set the proper labels to differentiate between messages.

Other additions
================

* `thoth/investigator/<message_name>/__init__.py`, please add the function for parsing messages
