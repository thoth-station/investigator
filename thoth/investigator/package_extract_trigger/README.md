# PackageExtractTriggerMessage

[PackageExtractTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/adviser_trigger.py)

This message received contains:

```python
image: str
environment_type: str
is_external: bool = True
verify_tls: bool = True
debug: bool = False
job_id: Optional[str] = None
origin: Optional[str] = None
registry_user: Optional[str] = None
registry_password: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to provide advice to user (human or bot):

- [package-extract](https://github.com/thoth-station/thoth-application/tree/master/package-extract) workflow
