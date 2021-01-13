# PackageReleasedMessage

[PackageReleasedMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/package_releases.py) is sent by:

- [package release producer](https://github.com/thoth-station/package-releases-job) to acquire knowledge on newly released package version from a certain index.

Available versions (see for message contents):

- [Current](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/package_releases.py)

Thoth investigator schedules the following workflows to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
- [Revsolver](https://github.com/thoth-station/revsolver) workflow
- [Security Indicator](https://github.com/thoth-station/si-aggregator) workflow
