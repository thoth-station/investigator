#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command and debug level
#

set -o nounset
set -o errexit
set -o errtrace
set -o pipefail
trap 'echo "Aborting due to errexit on line $LINENO. Exit code: $?" >&2' ERR

# TODO(pacospace) maybe this is a good inspiration: https://github.com/xwmx/bash-boilerplate/blob/master/bash-commands

FAUST_COMMAND="faust --web-host 0.0.0.0"
SUBCOMMAND=${SUBCOMMAND:-producer}
DEBUG_LEVEL=${DEBUG_LEVEL:-0}

if [ "$SUBCOMMAND" == "producer" ]
then
    if [ "$DEBUG_LEVEL" -eq 1 ]
    then
        exec ${FAUST_COMMAND} --debug --loglevel debug -A producer main
    else
        exec ${FAUST_COMMAND} -A producer main
    fi
elif [ "$SUBCOMMAND" = "consumer" ]
then
    if [ "$DEBUG_LEVEL" -eq 1 ]
    then
        exec ${FAUST_COMMAND} --debug --loglevel debug -A consumer worker
    else
        exec ${FAUST_COMMAND} -A consumer worker
    fi
fi
