# SolvedPackageMessage

[SolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/solved_package.py) is sent by:

- [solver](https://github.com/thoth-station/solver) when Thoth learn about new package version index solved.

This message received contains:

```python
package_name: str
package_version: str
index_url: str
solver: str
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to increase Thoth knowledge:

- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow
