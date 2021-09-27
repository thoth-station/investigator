# Changelog for Thoth's Template GitHub Project

## Release 0.15.1 (2021-09-27T20:30:11)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.15.0 (2021-09-14T18:23:33)
### Features
* add /halt endpoint for stopping consumption of specific messages manually
* add consumer offsets as metric to calculate consumer lag

## Release 0.14.4 (2021-08-24T12:26:56)
### Features
* Enable v5 of adviser trigger messaging

## Release 0.14.3 (2021-08-17T12:57:01)
### Features
* Fix halt in consumer

## Release 0.14.2 (2021-08-09T08:01:14)
### Features
* :arrow_up: auto dependencies for the investigator
* add option to pass list as ack on fail envvar
### Bug Fixes
* bug fix: passed message info did not match expected format

## [0.1.0] - 2019-Sep-11 - goern

### Added

all the things that you see...

## Release 0.1.1 (2020-06-25T18:54:56)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* :pushpin: Automatic update of dependency hypothesis from 5.16.0 to 5.18.1
* :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* :pushpin: Automatic update of dependency hypothesis from 5.16.0 to 5.18.1
* :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.4 to 1.4.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.12
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12

## Release 0.1.2 (2020-07-09T15:17:41)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.2 (#52)
* Remove not required parameters (#54)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.1 (#51)
* :pushpin: Automatic update of dependency hypothesis from 5.18.1 to 5.18.3 (#49)
* setup.py is not required if this isnt a package (#47)
* Create OWNERS

## Release 0.2.0 (2020-07-10T12:40:21)
* Correct mypy
* fixed some mypy errors
* fixed some flake8 errors
* :arrow_up: did a 'pre-commit autoupdate'
* removed setup.py, see https://github.com/thoth-station/unknown-package-handler/pull/47\#issuecomment-650215895
* :sparkles: using pre-commit now, removed coala config
* Modify code and update README after renaming the component
* :pushpin: Automatic update of dependency thoth-storages from 0.24.2 to 0.24.3 (#57)
* :pushpin: Automatic update of dependency hypothesis from 5.18.3 to 5.19.0 (#53)

## Release 0.2.1 (2020-07-10T17:03:41)
* minor missing piece (#67)
* Remove templates (#66)

## Release 0.2.2 (2020-07-11T13:14:44)
* Correct parameter from Kafka message

## Release 0.2.3 (2020-07-15T14:48:28)
* :pushpin: Automatic update of dependency hypothesis from 5.19.2 to 5.19.3 (#80)
* Add a few persistent metrics (#74)
* :pushpin: Automatic update of dependency hypothesis from 5.19.0 to 5.19.2 (#77)
* Make producer more asynchronous by creating all futures before awaiting (#75)
* include aicoe-ci configuration file

## Release 0.2.4 (2020-07-16T11:43:20)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#84)
* a little more roubust app.sh (#76)

## Release 0.2.5 (2020-07-16T20:42:24)
* Add Missing connection to database (#90)
* point to the right context path (#88)

## Release 0.2.6 (2020-07-17T15:20:36)
* Add more logging (#94)

## Release 0.2.7 (2020-07-22T10:22:55)
* Feature/metrics (#108)
* :pushpin: Automatic update of dependency hypothesis from 5.20.2 to 5.20.3 (#105)
* Schedule workflows (#103)
* :pushpin: Automatic update of dependency hypothesis from 5.20.1 to 5.20.2 (#102)
* :pushpin: Automatic update of dependency hypothesis from 5.20.0 to 5.20.1 (#100)

## Release 0.3.0 (2020-07-24T08:36:19)
* Update README (#120)
* Adjust app initialization with new implementation in thoth-messaging (#115)
* Add tests (#116)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#119)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#117)
* :pushpin: Automatic update of dependency hypothesis from 5.20.3 to 5.21.0 (#118)
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.7 to 0.5.0 (#114)

## Release 0.4.0 (2020-07-27T15:38:48)
* Consider all versions explicitly and loop backward from latest (#124)

## Release 0.4.1 (2020-08-21T15:15:14)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.4 (#154)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#150)
* Add investigate solved message methods (#143)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.4 (#153)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.3 to 0.6.5 (#152)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#147)
* :pushpin: Automatic update of dependency hypothesis from 5.24.2 to 5.27.0 (#151)
* :pushpin: Automatic update of dependency hypothesis from 5.24.0 to 5.24.2 (#146)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#144)
* use sorting method from thoth-python (#142)
* :pushpin: Automatic update of dependency hypothesis from 5.23.2 to 5.24.0 (#141)
* :pushpin: Automatic update of dependency hypothesis from 5.23.2 to 5.24.0 (#136)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#138)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.2 to 0.6.3 (#137)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.1 (#135)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#134)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.2 to 0.6.3 (#133)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#132)
* :pushpin: Automatic update of dependency hypothesis from 5.21.0 to 5.23.2 (#131)
* :pushpin: Automatic update of dependency hypothesis from 5.21.0 to 5.23.2 (#128)

## Release 0.4.2 (2020-08-24T07:41:43)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.4 to 0.25.5 (#161)
* Add methods to handle Unrevsolved Package Message (#159)

## Release 0.4.3 (2020-09-09T14:42:17)
### Features
* change directory name
* create directory investigator
* remove import of service version
* change all to relative imports
* include thoth-sourcemanagement
* add service version to __all__
* add component_name and service_version
* add dev guide for parsing new message
* add processing of advise justification messages
### Bug Fixes
* init logger after app initalizes
### Improvements
* simplify __init__.py
* use relative import for metrics
* new structure for investigator and move package update consumer
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.17.0 to 0.17.2 (#176)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.7 to 0.7.0 (#177)
* :pushpin: Automatic update of dependency hypothesis from 5.29.1 to 5.30.0 (#174)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.0 (#171)
* :pushpin: Automatic update of dependency hypothesis from 5.28.0 to 5.29.1 (#173)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.5 to 0.6.7 (#172)
* :pushpin: Automatic update of dependency hypothesis from 5.27.0 to 5.28.0 (#165)
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#163)
* :pushpin: Automatic update of dependency hypothesis from 5.27.0 to 5.28.0 (#162)

## Release 0.4.4 (2020-09-10T09:42:39)
### Features
* add component and version to message (#185)

## Release 0.4.5 (2020-09-11T14:15:26)
### Features
* Add Investigate AdviserReRunMessage to Investigator (#192)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.33.2 to 5.35.0 (#193)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.6 to 0.25.7 (#191)
* :pushpin: Automatic update of dependency thoth-common from 0.18.0 to 0.18.1 (#190)

## Release 0.4.6 (2020-09-16T17:15:11)
### Features
* add consumers for workflow triggers (#214)
* Remove SI scheduling from UnresolvedPackageMessage (#221)
* Update .thoth.yaml (#218)
* Added logic to process SI Unanalyzed messages (#212)
* handle package released messages (#206)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.2 to 0.7.3 (#222)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.9 to 0.25.10 (#220)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.2 (#210)
* :pushpin: Automatic update of dependency hypothesis from 5.35.2 to 5.35.3 (#213)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.0 to 0.3.1 (#216)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.8 to 0.25.9 (#211)
* :pushpin: Automatic update of dependency thoth-common from 0.18.3 to 0.19.0 (#209)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.7 to 0.25.8 (#207)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.7 to 0.25.8 (#199)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.18.3 (#198)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#200)
* :pushpin: Automatic update of dependency hypothesis from 5.35.0 to 5.35.2 (#202)
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#196)

## Release 0.4.7 (2020-09-17T07:57:44)
### Bug Fixes
* patch fix the variable reference for metrics (#225)

## Release 0.4.8 (2020-09-22T16:31:01)
### Features
* Adjust links (#245)
* Adjust logging (#237)
### Improvements
* Update and refactor docs (#233)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.1 to 0.3.2 (#244)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.10 to 0.25.11 (#240)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.1 to 0.3.2 (#241)
* :pushpin: Automatic update of dependency hypothesis from 5.35.3 to 5.35.4 (#242)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.3 to 0.7.6 (#230)

## Release 0.4.9 (2020-09-24T16:46:52)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.35.4 to 5.36.0 (#254)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#253)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#250)
* :pushpin: Automatic update of dependency hypothesis from 5.35.4 to 5.36.0 (#251)

## Release 0.4.10 (2020-09-25T05:55:49)
### Features
* correct the investigate_unresolved_package import (#259)

## Release 0.4.11 (2020-09-25T18:25:23)
### Features
* Correct wrong message (#263)

## Release 0.4.12 (2020-09-25T18:59:04)
### Improvements
* make func async (#269)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.36.0 to 5.36.1 (#268)

## Release 0.4.13 (2020-09-30T07:11:26)
### Features
* Add images for Thoth Learning using Kafka (#282)
* add all env variables to README (#273)
### Bug Fixes
* fixed a typo
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-storages from 0.25.12 to 0.25.13 (#280)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.7 to 0.7.8 (#279)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.11 to 0.25.12 (#276)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#278)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.6 to 0.7.7 (#277)

## Release 0.4.14 (2020-09-30T10:05:06)
### Features
* Remove parameter not existing in message (#288)
* Describe User-API Investigator interaction (#286)

## Release 0.5.0 (2020-09-30T16:23:25)
### Features
* Add workflow namespace variables for quota limit check (#291)

## Release 0.5.1 (2020-10-01T10:20:19)
### Features
* Consume new message UpdateProvidesSourceDistroMessage (#281)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.9 (#296)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#295)

## Release 0.5.2 (2020-10-05T07:03:44)
### Improvements
* use async prometheus (#275)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.36.1 to 5.37.0 (#304)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#303)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#302)

## Release 0.5.3 (2020-10-05T08:30:36)
### Features
* Update readme si (#299)
* Add missing metrics (#308)

## Release 0.5.4 (2020-10-06T19:16:52)
### Features
* Add metrics to see what workflows are scheduled (#313)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#318)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#317)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#316)

## Release 0.5.5 (2020-10-09T16:33:25)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.37.0 to 5.37.1 (#323)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1 (#322)

## Release 0.6.0 (2020-10-28T15:40:09)
### Features
* add KPostOffice to list of maintainers (#349)
* Correct link (#345)
* Confluent rework (#344)
* Add kebechet run url (#342)
* Add docs for Thoth investigator (#330)
* Remove producer from investigator (#329)
### Automatic Updates
* :pushpin: Automatic update of dependency hypothesis from 5.38.0 to 5.38.1 (#354)
* :pushpin: Automatic update of dependency thoth-messaging from 0.8.0 to 0.8.2 (#353)
* :pushpin: Automatic update of dependency hypothesis from 5.37.4 to 5.38.0 (#347)
* :pushpin: Automatic update of dependency hypothesis from 5.37.3 to 5.37.4 (#341)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.13 to 0.8.0 (#340)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#338)
* :pushpin: Automatic update of dependency hypothesis from 5.37.1 to 5.37.3 (#332)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.12 to 0.7.13 (#331)
* :pushpin: Automatic update of dependency mypy from 0.782 to 0.790 (#328)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.11 to 0.7.12 (#327)

## Release 0.6.1 (2020-11-30T14:53:24)
### Features
* adjust aicoe-ci and update the packages (#386)
* port to python 38 (#382)
* add **kwargs so all funcs can be called the same (#375)
* Move to thoth namespace (#361)
* Added kebechet administrator triggers to message investigators (#357)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest-mypy from 0.7.0 to 0.8.0 (#380)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.4.0 to 0.4.1 (#379)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.3 to 0.4.0 (#378)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.3 to 0.4.0 (#377)
* :pushpin: Automatic update of dependency thoth-storages from 0.26.0 to 0.26.1 (#376)
* :pushpin: Automatic update of dependency hypothesis from 5.41.0 to 5.41.2 (#374)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.16 to 0.26.0 (#373)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#372)
* :pushpin: Automatic update of dependency hypothesis from 5.40.0 to 5.41.0 (#371)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#370)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.25.16 (#369)
* :pushpin: Automatic update of dependency hypothesis from 5.38.1 to 5.40.0 (#366)
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#365)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#364)

## Release 0.7.0 (2021-01-12T13:20:04)
### Features
* :arrow_up: Automatic update of dependencies by kebechet. (#395)
* :arrow_up: Automatic update of dependencies by kebechet. (#392)
* Remove use-before-declared linter warning (#390)
### Improvements
* Do not use mutable arguments in functions (#391)

## Release 0.8.0 (2021-01-12T18:52:56)
### Features
* Buildlog analysis trigger (#393)
* :arrow_up: Automatic update of dependencies by kebechet. (#403)
* Manual update of dependencies (#405)
* :arrow_up: Automatic update of dependencies by kebechet. (#399)
### Improvements
* removed bissenbay, thanks for your contributions!

## Release 0.8.1 (2021-01-13T18:21:03)
### Features
* analsysis->analysis (#410)

## Release 0.8.2 (2021-01-14T11:26:47)
### Features
* :arrow_up: Automatic update of dependencies by kebechet. (#415)
* remove message contents (link instead) (#409)
* :arrow_up: Automatic update of dependencies by kebechet. (#413)
### Improvements
* Update dependencies to have more recent thoth-common (#418)

## Release 0.9.0 (2021-01-20T20:18:11)
### Features
* Add metric schema (#428)
* :arrow_up: Automatic update of dependencies by kebechet. (#427)
* :arrow_up: Automatic update of dependencies by kebechet. (#423)
* decs are applied inside-out (#424)
### Bug Fixes
* retry on exceptions and other error handling (#389)

## Release 0.9.1 (2021-01-26T09:49:05)
### Features
* Standardize metrics for revision check (#434)
* :arrow_up: Automatic update of dependencies by kebechet. (#436)

## Release 0.9.2 (2021-02-20T07:09:39)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#446)
* add handler for inspection complete messages (#433)
* :arrow_up: Automatic update of dependencies by Kebechet (#444)
* :arrow_up: Automatic update of dependencies by Kebechet (#443)
* Add missing title to Kebechet template
* :arrow_up: Automatic update of dependencies by Kebechet (#440)

## Release 0.10.0 (2021-02-25T20:20:34)
### Features
* Manual dependency update (#457)
* Bump adviser re-run and provenance-checker message versions
### Bug Fixes
* Do not pass arguments that are prepared in adviser container

## Release 0.10.1 (2021-03-21T18:55:29)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#473)
* relock the dependencies (#471)
* add new args to function call (#469)
* :arrow_up: Automatic update of dependencies by Kebechet (#461)
* :arrow_up: update pre-commit plugins, CI related configs (#466)
* if handler hasn't been registered treat it the same as messagea excep… (#465)
### Other
* Add code for switching modes (handler functions) in investigator (#467)

## Release 0.11.0 (2021-03-31T21:09:00)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#482)
* :arrow_up: Automatic update of dependencies by Kebechet (#477)
* add new function args to call (#476)

## Release 0.11.1 (2021-04-12T19:20:33)
### Features
* Constrain thoth-messaging to <=0.13
* Changes for publishing on thoth-station.ninja (#488)
* :arrow_up: Automatic update of dependencies by Kebechet (#487)
* constrain thoth-messaging (#478)
* :arrow_up: Automatic update of dependencies by Kebechet (#486)
* :arrow_up: Automatic update of dependencies by Kebechet (#485)
### Improvements
* use function as handler for all versions of message (#480)

## Release 0.11.2 (2021-04-12T20:13:46)
### Features
* Adviser trigger message v4 (#492)

## Release 0.12.0 (2021-05-03T03:40:49)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#504)
* :arrow_up: Automatic update of dependencies by Kebechet (#502)
* F/pydantic consumer (#500)
* :arrow_up: Automatic update of dependencies by Kebechet (#499)
* Remove adviser re run message consumer (#498)
* :arrow_up: Automatic update of dependencies by Kebechet (#497)
* Fix type for the authenticated parameter (#495)
### Bug Fixes
* Relock the dependencies for fix sqlalchemy-utils (#508)

## Release 0.12.1 (2021-05-10T04:27:12)
### Features
* messages are no longer classes (#515)
* :arrow_up: Automatic update of dependencies by Kebechet (#512)

## Release 0.13.0 (2021-06-03T17:35:26)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :hatched_chick: update the prow resource limits (#519)
* loop being deprecated, use asyncio.run instead (#514)
### Other
* remove thoth-sourcemanagement from dependencies (#521)

## Release 0.13.1 (2021-06-14T19:19:35)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* remove inner loop which loops over registered indexes
* :arrow_up: Automatic update of dependencies by Kebechet
* expect only single index in message contents

## Release 0.13.2 (2021-07-01T02:31:48)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* Deprecate qeb-hwt workflow
* :arrow_up: Automatic update of dependencies by Kebechet
* :medal_sports: set badges for easy access to content (#538)
* mark missing packages and schedule keb admin

## Release 0.14.0 (2021-07-02T09:02:16)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Release of version 0.13.2 (#545)
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* Deprecate qeb-hwt workflow
* :arrow_up: Automatic update of dependencies by Kebechet
* :medal_sports: set badges for easy access to content (#538)
* Release of version 0.13.1
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* remove inner loop which loops over registered indexes
* mark missing packages and schedule keb admin
* :arrow_up: Automatic update of dependencies by Kebechet
* expect only single index in message contents
* Release of version 0.13.0
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :hatched_chick: update the prow resource limits (#519)
* loop being deprecated, use asyncio.run instead (#514)
* Release of version 0.12.1 (#518)
* :arrow_up: Automatic update of dependencies by Kebechet (#517)
* messages are no longer classes (#515)
* :arrow_up: Automatic update of dependencies by Kebechet (#512)
* Release of version 0.12.0 (#510)
* :arrow_up: Automatic update of dependencies by Kebechet (#504)
* :arrow_up: Automatic update of dependencies by Kebechet (#502)
* F/pydantic consumer (#500)
* :arrow_up: Automatic update of dependencies by Kebechet (#499)
* Remove adviser re run message consumer (#498)
* :arrow_up: Automatic update of dependencies by Kebechet (#497)
* Fix type for the authenticated parameter (#495)
* Release of version 0.11.2 (#494)
* Adviser trigger message v4 (#492)
* Release of version 0.11.1 (#491)
* Constrain thoth-messaging to <=0.13
* Changes for publishing on thoth-station.ninja (#488)
* :arrow_up: Automatic update of dependencies by Kebechet (#487)
* constrain thoth-messaging (#478)
* :arrow_up: Automatic update of dependencies by Kebechet (#486)
* :arrow_up: Automatic update of dependencies by Kebechet (#485)
* Release of version 0.11.0 (#484)
* :arrow_up: Automatic update of dependencies by Kebechet (#482)
* :arrow_up: Automatic update of dependencies by Kebechet (#477)
* add new function args to call (#476)
* Release of version 0.10.1 (#475)
* :arrow_up: Automatic update of dependencies by Kebechet (#473)
* relock the dependencies (#471)
* add new args to function call (#469)
* :arrow_up: Automatic update of dependencies by Kebechet (#461)
* :arrow_up: update pre-commit plugins, CI related configs (#466)
* if handler hasn't been registered treat it the same as messagea excep… (#465)
* Release of version 0.10.0
* Manual dependency update (#457)
* Bump adviser re-run and provenance-checker message versions
* Release of version 0.9.2 (#449)
* :arrow_up: Automatic update of dependencies by Kebechet (#448)
* :arrow_up: Automatic update of dependencies by Kebechet (#446)
* add handler for inspection complete messages (#433)
* :arrow_up: Automatic update of dependencies by Kebechet (#444)
* :arrow_up: Automatic update of dependencies by Kebechet (#443)
* Add missing title to Kebechet template
* :arrow_up: Automatic update of dependencies by Kebechet (#440)
* Release of version 0.9.1 (#438)
* Standardize metrics for revision check (#434)
* :arrow_up: Automatic update of dependencies by kebechet. (#436)
* Release of version 0.9.0 (#432)
* :arrow_up: Automatic update of dependencies by kebechet. (#431)
* Add metric schema (#428)
* :arrow_up: Automatic update of dependencies by kebechet. (#427)
* :arrow_up: Automatic update of dependencies by kebechet. (#423)
* decs are applied inside-out (#424)
* Release of version 0.8.2 (#420)
* Add "Kebechet update" and "Kebechet info" issue templates (#417)
* :arrow_up: Automatic update of dependencies by kebechet. (#415)
* remove message contents (link instead) (#409)
* :arrow_up: Automatic update of dependencies by kebechet. (#413)
* Release of version 0.8.1 (#414)
* analsysis->analysis (#410)
* Release of version 0.8.0 (#408)
* Buildlog analysis trigger (#393)
* :arrow_up: Automatic update of dependencies by kebechet. (#403)
* Manual update of dependencies (#405)
* :arrow_up: Automatic update of dependencies by kebechet. (#399)
* Release of version 0.7.0 (#398)
* :arrow_up: Automatic update of dependencies by kebechet. (#397)
* :arrow_up: Automatic update of dependencies by kebechet. (#395)
* :arrow_up: Automatic update of dependencies by kebechet. (#392)
* Remove use-before-declared linter warning (#390)
* Release of version 0.6.1 (#388)
* adjust aicoe-ci and update the packages (#386)
* port to python 38 (#382)
* add **kwargs so all funcs can be called the same (#375)
* Move to thoth namespace (#361)
* Added kebechet administrator triggers to message investigators (#357)
* Release of version 0.6.0 (#360)
* add KPostOffice to list of maintainers (#349)
* Correct link (#345)
* Confluent rework (#344)
* Add kebechet run url (#342)
* Add docs for Thoth investigator (#330)
* Remove producer from investigator (#329)
* Release of version 0.5.5 (#325)
* Release of version 0.5.4 (#320)
* Add metrics to see what workflows are scheduled (#313)
* Release of version 0.5.3 (#310)
* Update readme si (#299)
* Add missing metrics (#308)
* Release of version 0.5.2 (#307)
* Release of version 0.5.1
* Consume new message UpdateProvidesSourceDistroMessage (#281)
* Release of version 0.5.0 (#293)
* Add workflow namespace variables for quota limit check (#291)
* Release of version 0.4.14 (#290)
* Remove parameter not existing in message (#288)
* Describe User-API Investigator interaction (#286)
* Release of version 0.4.13 (#285)
* Add images for Thoth Learning using Kafka (#282)
* add all env variables to README (#273)
* Release of version 0.4.12 (#271)
* Release of version 0.4.11 (#267)
* Correct wrong message (#263)
* Release of version 0.4.10 (#261)
* add decorator to submit workflow to wait for pending limit (#215)
* correct the investigate_unresolved_package import (#259)
* Release of version 0.4.9 (#258)
* Release of version 0.4.8 (#248)
* Adjust links (#245)
* Adjust logging (#237)
* Release of version 0.4.7 (#228)
* Release of version 0.4.6 (#224)
* add consumers for workflow triggers (#214)
* Remove SI scheduling from UnresolvedPackageMessage (#221)
* Update .thoth.yaml (#218)
* Added logic to process SI Unanalyzed messages (#212)
* handle package released messages (#206)
* Release of version 0.4.5 (#195)
* Add Investigate AdviserReRunMessage to Investigator (#192)
* Release of version 0.4.4 (#189)
* add component and version to message (#185)
* Release of version 0.4.3
* change directory name
* create directory investigator
* remove import of service version
* change all to relative imports
* include thoth-sourcemanagement
* add service version to __all__
* add component_name and service_version
* add dev guide for parsing new message
* add processing of advise justification messages
* Release of version 0.4.2 (#164)
* Release of version 0.4.1 (#158)
* Release of version 0.4.0 (#129)
* Consider all versions explicitly and loop backward from latest (#124)
* Release of version 0.3.0 (#122)
* Update README (#120)
* Adjust app initialization with new implementation in thoth-messaging (#115)
* Release of version 0.2.7 (#110)
* Feature/metrics (#108)
* Schedule workflows (#103)
* Release of version 0.2.6 (#98)
* Release of version 0.2.5 (#93)
* Add Missing connection to database (#90)
* point to the right context path (#88)
* Release of version 0.2.4 (#86)
* a little more roubust app.sh (#76)
* Release of version 0.2.3 (#82)
* Add a few persistent metrics (#74)
* include aicoe-ci configuration file
* Release of version 0.2.2 (#73)
* Correct parameter from Kafka message
* Release of version 0.2.1 (#69)
* Remove templates (#66)
* Release of version 0.2.0 (#65)
* Correct mypy
* :arrow_up: did a 'pre-commit autoupdate'
* Release of version 0.1.2 (#56)
* Remove not required parameters (#54)
* setup.py is not required if this isnt a package (#47)
* Create OWNERS
* Release of version 0.1.1
* added a 'tekton trigger tag_release pipeline issue'
* Add outputs typing
* update values
* add version
* Add consumer
* add packages
* Create unsolved package handler workflow template for adviser workflow
* add setup.py
* add ApiGorup
* move to repo
* little changes
* Add JSON_FILE_PATH env variable
* Remove old env variables
* add checks
* correct imports
* correct name
* Add App.sh to run component
* Correct assertion
* Adjust env variables
* small changes
* Use single line message string
* Add openshift templates
* Add tests
* Update zuul
* Update README
* Add requirements
* Add requirements
* Update .zuul.yaml
* Update .zuul.yaml
### Bug Fixes
* Relock the dependencies for fix sqlalchemy-utils (#508)
* Do not pass arguments that are prepared in adviser container
* retry on exceptions and other error handling (#389)
* fixed a typo
* patch fix the variable reference for metrics (#225)
* init logger after app initalizes
* fixed some mypy errors
* fixed some flake8 errors
### Improvements
* use function as handler for all versions of message (#480)
* Update dependencies to have more recent thoth-common (#418)
* removed bissenbay, thanks for your contributions!
* Do not use mutable arguments in functions (#391)
* use async prometheus (#275)
* make func async (#269)
* Update and refactor docs (#233)
* simplify __init__.py
* use relative import for metrics
* new structure for investigator and move package update consumer
* Add methods to handle Unrevsolved Package Message (#159)
* Add investigate solved message methods (#143)
* use sorting method from thoth-python (#142)
* Add tests (#116)
* Add more logging (#94)
* Make producer more asynchronous by creating all futures before awaiting (#75)
* minor missing piece (#67)
* removed setup.py, see https://github.com/thoth-station/unknown-package-handler/pull/47\#issuecomment-650215895
* :sparkles: using pre-commit now, removed coala config
* Add methods for consumer
* Adjust test
* use solver
* use Job
* Adjust main method
* Add Pipfile and Pipfile.lock
* Update README and removed files
### Non-functional
* Split main producer method for testing
### Other
* remove thoth-sourcemanagement from dependencies (#521)
* Add code for switching modes (handler functions) in investigator (#467)
* Modify code and update README after renaming the component
* remove variables
* remove condition
### Automatic Updates
* :pushpin: Automatic update of dependency pytest-mypy from 0.7.0 to 0.8.0 (#380)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.4.0 to 0.4.1 (#379)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.3 to 0.4.0 (#378)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.3 to 0.4.0 (#377)
* :pushpin: Automatic update of dependency thoth-storages from 0.26.0 to 0.26.1 (#376)
* :pushpin: Automatic update of dependency hypothesis from 5.41.0 to 5.41.2 (#374)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.16 to 0.26.0 (#373)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#372)
* :pushpin: Automatic update of dependency hypothesis from 5.40.0 to 5.41.0 (#371)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#370)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.25.16 (#369)
* :pushpin: Automatic update of dependency hypothesis from 5.38.1 to 5.40.0 (#366)
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#365)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#364)
* :pushpin: Automatic update of dependency hypothesis from 5.38.0 to 5.38.1 (#354)
* :pushpin: Automatic update of dependency thoth-messaging from 0.8.0 to 0.8.2 (#353)
* :pushpin: Automatic update of dependency hypothesis from 5.37.4 to 5.38.0 (#347)
* :pushpin: Automatic update of dependency hypothesis from 5.37.3 to 5.37.4 (#341)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.13 to 0.8.0 (#340)
* :pushpin: Automatic update of dependency thoth-common from 0.20.1 to 0.20.2 (#338)
* :pushpin: Automatic update of dependency hypothesis from 5.37.1 to 5.37.3 (#332)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.12 to 0.7.13 (#331)
* :pushpin: Automatic update of dependency mypy from 0.782 to 0.790 (#328)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.11 to 0.7.12 (#327)
* :pushpin: Automatic update of dependency hypothesis from 5.37.0 to 5.37.1 (#323)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.1 (#322)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#318)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#317)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.10 to 0.7.11 (#316)
* :pushpin: Automatic update of dependency hypothesis from 5.36.1 to 5.37.0 (#304)
* :pushpin: Automatic update of dependency pytest from 6.1.0 to 6.1.1 (#303)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.14 to 0.25.15 (#302)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.9 (#296)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#295)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.12 to 0.25.13 (#280)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.7 to 0.7.8 (#279)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.11 to 0.25.12 (#276)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#278)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.6 to 0.7.7 (#277)
* :pushpin: Automatic update of dependency hypothesis from 5.36.0 to 5.36.1 (#268)
* :pushpin: Automatic update of dependency hypothesis from 5.36.0 to 5.36.1 (#266)
* :pushpin: Automatic update of dependency hypothesis from 5.35.4 to 5.36.0 (#254)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#253)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#250)
* :pushpin: Automatic update of dependency hypothesis from 5.35.4 to 5.36.0 (#251)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.1 to 0.3.2 (#244)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.10 to 0.25.11 (#240)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.1 to 0.3.2 (#241)
* :pushpin: Automatic update of dependency hypothesis from 5.35.3 to 5.35.4 (#242)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.3 to 0.7.6 (#230)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.2 to 0.7.3 (#222)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.9 to 0.25.10 (#220)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.2 (#210)
* :pushpin: Automatic update of dependency hypothesis from 5.35.2 to 5.35.3 (#213)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.0 to 0.3.1 (#216)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.8 to 0.25.9 (#211)
* :pushpin: Automatic update of dependency thoth-common from 0.18.3 to 0.19.0 (#209)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.7 to 0.25.8 (#207)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.7 to 0.25.8 (#199)
* :pushpin: Automatic update of dependency thoth-common from 0.18.2 to 0.18.3 (#198)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#200)
* :pushpin: Automatic update of dependency hypothesis from 5.35.0 to 5.35.2 (#202)
* :pushpin: Automatic update of dependency thoth-common from 0.18.1 to 0.18.2 (#196)
* :pushpin: Automatic update of dependency hypothesis from 5.33.2 to 5.35.0 (#193)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.6 to 0.25.7 (#191)
* :pushpin: Automatic update of dependency thoth-common from 0.18.0 to 0.18.1 (#190)
* :pushpin: Automatic update of dependency thoth-common from 0.17.3 to 0.18.0 (#188)
* :pushpin: Automatic update of dependency hypothesis from 5.30.0 to 5.33.2
* :pushpin: Automatic update of dependency thoth-common from 0.17.2 to 0.17.3
* :pushpin: Automatic update of dependency thoth-common from 0.17.0 to 0.17.2 (#176)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.7 to 0.7.0 (#177)
* :pushpin: Automatic update of dependency hypothesis from 5.29.1 to 5.30.0 (#174)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.0 (#171)
* :pushpin: Automatic update of dependency hypothesis from 5.28.0 to 5.29.1 (#173)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.5 to 0.6.7 (#172)
* :pushpin: Automatic update of dependency hypothesis from 5.27.0 to 5.28.0 (#165)
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#163)
* :pushpin: Automatic update of dependency hypothesis from 5.27.0 to 5.28.0 (#162)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.4 to 0.25.5 (#161)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.4 (#154)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#150)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.0 to 0.25.4 (#153)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.3 to 0.6.5 (#152)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#147)
* :pushpin: Automatic update of dependency hypothesis from 5.24.2 to 5.27.0 (#151)
* :pushpin: Automatic update of dependency hypothesis from 5.24.0 to 5.24.2 (#146)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#144)
* :pushpin: Automatic update of dependency hypothesis from 5.23.2 to 5.24.0 (#141)
* :pushpin: Automatic update of dependency hypothesis from 5.23.2 to 5.24.0 (#136)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#138)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.2 to 0.6.3 (#137)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.1 (#135)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.0 (#134)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.2 to 0.6.3 (#133)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#132)
* :pushpin: Automatic update of dependency hypothesis from 5.21.0 to 5.23.2 (#131)
* :pushpin: Automatic update of dependency hypothesis from 5.21.0 to 5.23.2 (#128)
* :pushpin: Automatic update of dependency thoth-messaging from 0.6.0 to 0.6.2 (#127)
* :pushpin: Automatic update of dependency thoth-messaging from 0.5.0 to 0.6.0 (#123)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#119)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#117)
* :pushpin: Automatic update of dependency hypothesis from 5.20.3 to 5.21.0 (#118)
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.7 to 0.5.0 (#114)
* :pushpin: Automatic update of dependency hypothesis from 5.20.2 to 5.20.3 (#105)
* :pushpin: Automatic update of dependency hypothesis from 5.20.1 to 5.20.2 (#102)
* :pushpin: Automatic update of dependency hypothesis from 5.20.0 to 5.20.1 (#100)
* :pushpin: Automatic update of dependency hypothesis from 5.19.3 to 5.20.0 (#99)
* :pushpin: Automatic update of dependency hypothesis from 5.19.3 to 5.20.0 (#97)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.3 to 0.24.4 (#96)
* :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#85)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#84)
* :pushpin: Automatic update of dependency hypothesis from 5.19.2 to 5.19.3 (#80)
* :pushpin: Automatic update of dependency hypothesis from 5.19.0 to 5.19.2 (#77)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.2 to 0.24.3 (#57)
* :pushpin: Automatic update of dependency hypothesis from 5.18.3 to 5.19.0 (#53)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.2 (#52)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.1 (#51)
* :pushpin: Automatic update of dependency hypothesis from 5.18.1 to 5.18.3 (#49)
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* :pushpin: Automatic update of dependency thoth-common from 0.13.12 to 0.13.13
* :pushpin: Automatic update of dependency hypothesis from 5.16.0 to 5.18.1
* :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* :pushpin: Automatic update of dependency hypothesis from 5.16.0 to 5.18.1
* :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.4 to 1.4.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.24.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.12
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* :pushpin: Automatic update of dependency thoth-common from 0.13.7 to 0.13.8
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12
* :pushpin: Automatic update of dependency hypothesis from 5.15.1 to 5.16.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.6 to 0.13.7
* :pushpin: Automatic update of dependency pytest-cov from 2.8.1 to 2.9.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.4 to 0.13.6
* :pushpin: Automatic update of dependency thoth-storages from 0.22.10 to 0.22.11
* :pushpin: Automatic update of dependency hypothesis from 5.15.0 to 5.15.1
* :pushpin: Automatic update of dependency hypothesis from 5.14.0 to 5.15.0
* :pushpin: Automatic update of dependency thoth-common from 0.13.3 to 0.13.4
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.4 to 0.3.6
* :pushpin: Automatic update of dependency thoth-common from 0.13.2 to 0.13.3
* :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.2 to 0.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.13.1

## Release 0.14.1 (2021-07-30T10:03:07)
### Features
* Exclude docs/
* Adjust CI prow
* :arrow_up: Automatic update of dependencies by Kebechet (#562)
* rename from 'paused' to 'halted'
* :arrow_up: Automatic update of dependencies by Kebechet
* add docs for  envvar and  endpoint
* :arrow_up: Automatic update of dependencies by Kebechet
### Other
* remove unusued parameters
