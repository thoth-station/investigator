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

Consumer is currently able to handle the following Kafka messages:

#### Configuration

- See [thoth-messaging](https://github.com/thoth-station/messaging)
- Faust Windowed Tables (see [here](https://faust.readthedocs.io/en/latest/userguide/tables.html))
  - `THOTH_INVESTIGATOR_WINDOW_EXPIRATION`: Set time until message offset window expires
  - `THOTH_INVESTIGATOR_TABLE_WINDOW`: The amount of time that a single table window covers
- `THOTH_GITHUB_PRIVATE_TOKEN`: token for authenticating actions on GitHub repositories
- `THOTH_GITLAB_PRIVATE_TOKEN`: token for authenticating actions on GitLab repositories

#### UnresolvedPackageMessage

- [UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py).

This message received contains:

```python
package_name: str
package_version: Optional[str]
index_url: Optional[List[str]]
solver: Optional[str]
component_name: str
service_version: str
```

Thoth investigator checks Thoth knowledge Graph and decides which workflows need to be scheduled to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
- [Revsolver](https://github.com/thoth-station/revsolver) workflow
- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow

#### UnrevsolvedPackageMessage

- [UnrevsolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unrevsolved_package.py).

This message received contains:

```python
package_name: str
package_version: str
component_name: str
service_version: str
```

Thoth investigator checks Thoth knowledge Graph and decides which workflows need to be scheduled to increase Thoth knowledge:

- [Revsolver](https://github.com/thoth-station/revsolver) workflow

#### SolvedPackageMessage

- [SolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/solved_package.py).

This message received contains:

```python
package_name: str
package_version: str
index_url: str
solver: str
component_name: str
service_version: str
```

Thoth investigator checks Thoth knowledge Graph and decides which workflows need to be scheduled to increase Thoth knowledge:

- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow

#### AdviseJustificationMessage

- [AdviseJustificationMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/advise_justification.py)

This message received contains:

```python
message: str
justification_type: str
count: int
component_name: str
service_version: str
```

These messages get processed to update advise justification metrics (`advise_justification_type_number`)

#### HashMismatchMessage

- [HashMismatchMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/hash_mismatch.py)

This message received contains:

```python
index_url: str
package_name: str
package_version: str
missing_from_source: List[str]
missing_from_database: List[str]
component_name: str
service_version: str
```

If the hashes for a package don't match on the database and package index we schedule workflows and update database.

#### MissingPackageMessage

- [MissingPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/missing_package.py)

This message received contains:

```python
index_url: str
package_name: str
component_name: str
service_version: str
```

If package goes missing from a package index we mark all it as missing.

#### MissingVersionMessage

- [MissingVersionMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/missing_version.py)

This message received contains:

```python
index_url: str
package_name: str
package_version: str
component_name: str
service_version: str
```

If package version goes missing from a package index we mark it as missing.

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
