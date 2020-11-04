# MissingPackageMessage

[MissingPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/missing_package.py)

This message received contains:

```python
index_url: str
package_name: str
component_name: str
service_version: str
```

If package goes missing from a package index we mark all it as missing.
