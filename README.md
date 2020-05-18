# thoth-unresolved-package-handler

This repo contains two jobs:

    PRODUCER: Check if there are any unresolved packages in adviser report.
    It sends a message to Kafka with information relative to package and runtime environment to use for the solver to be scheduled.

    CONSUMER: Take messages from Kafka relative to package that need to be solved with priority and schedule solver for it.
