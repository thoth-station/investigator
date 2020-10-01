# UpdateProvidesSourceDistroMessage

- [UpdateProvidesSourceDistroMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/update_provides_src_distro.py)

This message received contains:

```python
package_name: str
package_version: str
index_url: str
value: bool
```

These messages get processed to change flag in Thoth database to know when a package cannot be SI analyzed because source distro is missing.
