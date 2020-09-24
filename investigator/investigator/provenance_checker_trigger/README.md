# ProvenanceCheckerTriggerMessage

[ProvenanceCheckerTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/provenance_checker_trigger.py)

This message received contains:

```python
application_stack: Dict[Any, Any]
debug: bool = False
origin: Optional[str] = None
whitelisted_sources: Optional[List[str]] = None
job_id: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to provide provenance checks to user (human or bot):

- [provenance-checker](https://github.com/thoth-station/thoth-application/tree/master/adviser) workflow
