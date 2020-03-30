# thoth-unresolved-package-handler

This repo contains two jobs:

    PRODUCER: Query the database for unresolved packages that need to be solved with priorities for a user. (Run in Argo workflow task through Python S2I)
    It sends a message to Kafka with information relative to package and runtime environment to use for the solver to be scheduled.

    CONSUMER: Take messages from Kafka relative to package that need to be solved with priority and schedule solver for it.
