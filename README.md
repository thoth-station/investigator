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

#### UnresolvedPackageMessage

- [UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py).

This message received contains:

```python
package_name: str
package_version: Optional[str]
index_url: Optional[List[str]]
solver: Optional[str]
```

Thoth investigator checks Thoth knowledge Graph and decides which workflows need to be scheduled to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
- [Revsolver](https://github.com/thoth-station/revsolver) workflow
- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow

#### SolvedPackageMessage

- [SolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/solved_package.py).

This message received contains:

```python
package_name: str
package_version: str
index_url: str
solver: str
```

Thoth investigator checks Thoth knowledge Graph and decides which workflows need to be scheduled to increase Thoth knowledge:

- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow
