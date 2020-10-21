# KebechetRunUrlTriggerMessage

[KebechetRunUrlTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/kebechet_run_url.py)

This message received contains:

```python
url = str
service_name = str
installation_id = str
job_id: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to run Kebechet bot:

- [kebechet run url](https://github.com/thoth-station/thoth-application/blob/master/kebechet/base/argo-workflows/kebechet-run-url.yaml) workflow
