# PackageReleasedMessage

[PackageReleasedMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/package_releases.py) is sent by:

- [package release producer](https://github.com/thoth-station/package-releases-job) to acquire knowledge on newly released package version from a certain index.

This message received contains:

```python
package_name: str
package_version: str
index_url: str
component_name: str
service_version: str
```

Thoth investigator schedules the following workflows to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
- [Revsolver](https://github.com/thoth-station/revsolver) workflow
- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow
