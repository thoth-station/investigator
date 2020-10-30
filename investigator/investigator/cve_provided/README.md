# CVEProvidedMessage

[CVEProvidedMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/cve_provided.py)

This message received contains:

```python
index_url: str
package_name: str
package_version: str
```

If we receive an CVEProvidedMessage we schedule KebechetAdministrator on all the affected repositories.
