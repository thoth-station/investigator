# AdviserTriggerMessage

[AdviserTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/adviser_trigger.py)

This message received contains:

```python
application_stack: Dict[Any, Any]
recommendation_type: str
dev: bool = False
debug: bool = False
count: Optional[int] = None
limit: Optional[int] = None
runtime_environment: Optional[Dict[Any, Any]] = None
library_usage: Optional[Dict[Any, Any]] = None
origin: Optional[str] = None
job_id: Optional[str] = None
limit_latest_versions: Optional[int] = None
github_event_type: Optional[str] = None
github_check_run_id: Optional[int] = None
github_installation_id: Optional[int] = None
github_base_repo_url: Optional[str] = None
re_run_adviser_id: Optional[str] = None
source_type: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to provide advice to user (human or bot):

- [adviser](https://github.com/thoth-station/thoth-application/tree/master/adviser) workflow
