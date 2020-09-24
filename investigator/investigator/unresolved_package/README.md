# UnresolvedPackageMessage

[UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py) is sent by:

- [graph-refresh producer](https://github.com/thoth-station/graph-refresh-job) to allow Thoth continuosly learn.

- [adviser](https://github.com/thoth-station/adviser) when Thoth is missing knowledge in providing an advice.

This message received contains:

```python
package_name: str
package_version: Optional[str]
index_url: Optional[List[str]]
solver: Optional[str]
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
