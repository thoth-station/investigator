# MissingVersionMessage

[MissingVersionMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/missing_version.py)

This message received contains:

```python
index_url: str
package_name: str
package_version: str
component_name: str
service_version: str
```

If package version goes missing from a package index we mark it as missing.
