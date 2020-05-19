#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command and debug level
#

if [ "$SUBCOMMAND" = "producer" ]
then
    if [ "$DEBUG_LEVEL" -eq 1]
    then
        exec faust --debug --loglevel debug -A producer main
    else
        exec faust -A producer main
elif [ "$SUBCOMMAND" = "consumer" ] && [ "$DEBUG_LEVEL" -eq 1]
then
    if [ "$DEBUG_LEVEL" -eq 1]
    then
        exec faust --debug --loglevel debug -A consumer worker
    else
       exec faust -A consumer worker
fi
