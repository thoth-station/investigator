# QebHwtTriggerMessage

[QebHwtTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/qebhwt_trigger.py)

This message received contains:

```python
github_event_type: str
github_check_run_id: int
github_installation_id: int
github_base_repo_url: str
github_head_repo_url: str
origin: str
revision: str
host: str
job_id: Optional[str] = None
component_name: str
service_version: str
```

Thoth investigator schedules the following workflow to provide advice to user (human or bot):

- [qeb-hwt](https://github.com/thoth-station/thoth-application/tree/master/qeb-hwt-github-app) workflow
