# KebechetTriggerMessage

[KebechetTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/kebechet_trigger.py)

This message received contains:

```python
webhook_payload: Dict[str, Any]
job_id: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to run Kebechet bot:

- [kebechet](https://github.com/thoth-station/thoth-application/tree/master/kebechet) workflow
