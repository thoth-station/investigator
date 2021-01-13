# UnresolvedPackageMessage

[UnresolvedPackageMessage](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py) is sent by:

- [graph-refresh producer](https://github.com/thoth-station/graph-refresh-job) to allow Thoth continuosly learn.

- [adviser](https://github.com/thoth-station/adviser) when Thoth is missing knowledge in providing an advice.

Available versions (see for message contents):

- [Current](https://github.com/thoth-station/messaging/blob/master/thoth/messaging/unresolved_package.py)

Thoth investigator schedules the following workflow to increase Thoth knowledge:

- [Solver](https://github.com/thoth-station/solver) workflow
