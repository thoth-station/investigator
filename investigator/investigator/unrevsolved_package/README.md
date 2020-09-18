# UnrevsolvedPackageMessage

[UnrevsolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unrevsolved_package.py) is sent by:

- [graph-refresh producer](https://github.com/thoth-station/graph-refresh-job) to allow Thoth continuosly learn.

This message received contains:

```python
package_name: str
package_version: str
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to increase Thoth knowledge:

- [Revsolver](https://github.com/thoth-station/revsolver) workflow
