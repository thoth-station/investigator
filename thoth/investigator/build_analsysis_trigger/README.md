# BuildAnalysisTriggerMessage

[BuildAnalysisTriggerMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/build_analysis_trigger.py)

This message received contains:

```python
output_image: Optional[str] = None,
base_image: Optional[str] = None,
registry_user: Optional[str] = None,
registry_password: Optional[str] = None,
registry_verify_tls: bool = True,
environment_type: Optional[str] = None,
buildlog_document_id: Optional[str] = None,
origin: Optional[str] = None,
job_id: Optional[str] = None,
```

Thoth investigator schedules the following workflow to provide advice to user (human or bot):

- [build-analysis](https://github.com/thoth-station/thoth-application/tree/master/build-analysis) workflow
