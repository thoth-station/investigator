# HashMismatchMessage

[HashMismatchMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/hash_mismatch.py)

This message received contains:

```python
index_url: str
package_name: str
package_version: str
missing_from_source: List[str]
missing_from_database: List[str]
component_name: str
service_version: str
```

If the hashes for a package don't match on the database and package index we schedule workflows and update database.
