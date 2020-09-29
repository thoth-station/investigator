# Investigator

Thoth Investigator is an agent sent out by Thoth to seek new information on packages, that will yield observations and knowledge to Thoth.

Thoth Investigator is called by Thoth components to gather new nessages after investigations about possible observations on packages.
These messages produced are sent out using Kafka.

Thoth Investigator centre of investigation receives those messages and after further investigation decides what actions need to be taken depending on the messages received,
so that Thoth can increase its knowledge.

This agent relies mainly on [thoth-messaging](https://github.com/thoth-station/messaging) to handle Kafka messages.

## Goals

This agent has two main goals:

- Produce event messages inside a workflow when some task related to a package release needs to be performed. (Producer)
- Receive messages from different components and take action depending on the info about a package. (Consumer)

### Producer

Producer is currently used in the following components in Thoth:

- [Adviser](https://github.com/thoth-station/adviser/tree/master/thoth/adviser) workflow, where it checks for any unresolved packages in the adviser report.
When the unresolved packages are present, it sends an [UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/a579a480819a9b35123e9002243f4bba6d082929/thoth/messaging/unresolved_package.py#L35)
to Kafka for each package release to be solved using Thoth [Solver](https://github.com/thoth-station/solver) workflow.

### Consumer

#### Environment Variables

- See [thoth-messaging](https://github.com/thoth-station/messaging)
- `THOTH_GITHUB_PRIVATE_TOKEN`: token for authenticating actions on GitHub repositories
- `THOTH_GITLAB_PRIVATE_TOKEN`: token for authenticating actions on GitLab repositories
- Enforcing a workflow limit:
  - `ARGO_PENDING_SLEEP_TIME`: amount of time we wait between checking the number of workflows in progress
  - `ARGO_PENDING_WORKFLOW_LIMIT`: limit to enforce on argo for total number of pending workflows

Consumer is currently able to handle the following Kafka messages focused on:

### Increase Thoth Knowledge

The following messages are sent by different Thoth components:

- [PackageReleasedMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/package_released/README.md).

- [UnresolvedPackageMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/unresolved_package/README.md).

- [UnrevsolvedPackageMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/unrevsolved_package/README.md).

- [SIUnanalyzedPackageMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/si_unanalyzed_package/README.md).

- [SolvedPackageMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/solved_package/README.md).

![IncreaseThothKnowledge](https://raw.githubusercontent.com/thoth-station/investigator/master/investigator/investigator/images/IncreaseThothKnowledge.jpg)

The image above shows how Thoth keeps learning automatically using two fundamental components that produce messages described in this section:

- [package release producer](https://github.com/thoth-station/package-releases-job) to acquire knowledge on newly released package version from a certain index.

- [graph-refresh producer](https://github.com/thoth-station/graph-refresh-job) to allow Thoth continuosly learn and keep the internal knowledge up to date.

### Monitor Thoth results and knowledge

The following message is sent by [advise reporter producer](https://github.com/thoth-station/advise-reporter) to show the use of recomendations across all Thoth integrations:

- [AdviseJustificationMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/advise_justification/README.md).

The following messages are sent by [package update producer](https://github.com/thoth-station/package-update-job) to keep knowledge in the database up to date:

- [HashMismatchMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/hash_mismatch/README.md).

- [MissingPackageMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/missing_package/README.md)

- [MissingVersionMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/missing_version/README.md)

The following message is sent by [solver](https://github.com/thoth-station/solver) when Thoth acquired all missing knowledge required to provide advice to a user (human or bot):

- [AdviserReRunMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/advise_justification/README.md).

### Trigger User requests

The following messages are sent by [User-API producer](https://github.com/thoth-station/user-api) when users (humans or bots)
interact with [Thoth integrations](https://github.com/thoth-station/adviser/blob/master/docs/source/integration.rst):

- [AdviserTriggerMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/adviser_trigger/README.md).

- [KebechetTriggerMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/kebechet_trigger/README.md)

- [PackageExtractTriggerMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/package_extract_trigger/README.md)

- [ProvenanceCheckerTriggerMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/provenance_checker_trigger/README.md)

- [QebHwtTriggerMessage](https://github.com/thoth-station/investigator/blob/master/investigator/investigator/qebhwt_trigger/README.md)

## Dev Guide

Most of the additions to this repository will entail adding new messages to process. That is what is being documented
here, if you feel that any information is missing please feel free to open an issue.

For each message there are two things you should implement:

1. message processing
2. consumer metrics

create a new directory in thoth/investigator which looks like this:

- message_name

  - `__init__.py`
  - investigate_<message_name>.py
  - metrics_<message_name>.py
  - `README.md` describing the message and what happens once consumed by investigator.

### Message Parsing

The implentation of this portion is highly specific to your own problem so not much can be advised in terms of rules
and regulations. In general calling the function `parse_<message_name>_message` is best practice.  Make sure to include
the three basic metrics to your function:

```python
@foo_exceptions.count_exceptions()
@foo_in_progress.track_inprogress()
def parse_foo_message(message):
    # do stuff
    foo_success.inc()

# <message_name> = foo
```

### Consumer Metrics

For consumer metrics you should at least have the following three:

- <message_name>_exceptions (prometheus Counter)
- <message_name>_success (prometheus Counter)
- <message_name>_in_progress (prometheus Gauge)

These are extensions of the metrics in `thoth/investigator/metrics.py`

The following is an example of a basic metrics file for a message `foo`:

```python
from ..metrics import in_progress, success, exceptions

foo_in_progress = in_progress.labels(message_type="foo")
foo_success = success.labels(message_type="foo")
foo_exceptions = exceptions.labels(message_type="foo")
```

You can add metrics as you see fit, but if the metric is not specific only to your messages please move it to
investigator/investigator/metrics.py and set the proper labels to differentiate between messages.

### Other additions

- `investigator/investigator/<message_name>/__init__.py`, please add the function for parsing messages
- `consumer.py`, add a new faust agent to process the message
