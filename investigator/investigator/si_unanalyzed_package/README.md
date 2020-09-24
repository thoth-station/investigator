# SIUnanalyzedPackageMessage

- [SIUnanalyzedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/si_unanalyzed_package.py) is sent by:

- [graph-refresh producer](https://github.com/thoth-station/graph-refresh-job) to allow Thoth continuosly learn.

This message received contains:

```python
package_name: str
package_version: str
index_url: str
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to increase Thoth knowledge:

- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow
