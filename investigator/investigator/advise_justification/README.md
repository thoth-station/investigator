# AdviseJustificationMessage

- [AdviseJustificationMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/advise_justification.py)

This message received contains:

```python
message: str
justification_type: str
count: int
component_name: str
service_version: str
```

These messages get processed to update advise justification metrics (`advise_justification_type_number`)
