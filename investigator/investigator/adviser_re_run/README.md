# AdviserReRunMessage

[AdviserReRunMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/adviser_re_run.py)

This message received contains:

```python
re_run_adviser_id: str
application_stack: Dict[Any, Any]
recommendation_type: str
runtime_environment: Optional[Dict[Any, Any]]
origin: Optional[str]
github_event_type: Optional[str]
github_check_run_id: Optional[int]
github_installation_id: Optional[int]
github_base_repo_url: Optional[str]
source_type: Optional[str]
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to provide advice to user (human or bot):

- [adviser](https://github.com/thoth-station/adviser) workflow
