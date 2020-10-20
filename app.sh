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

SUBCOMMAND=${SUBCOMMAND:-consumer}
DEBUG_LEVEL=${DEBUG_LEVEL:-0}
DEBUG_FLAGS=""

if [ "$DEBUG_LEVEL" -eq 1 ]; then
    DEBUG_FLAGS="--debug --loglevel debug"
fi

if [ "$SUBCOMMAND" == "consumer" ]; then
    exec faust ${DEBUG_FLAGS} -A consumer worker --web-host 0.0.0.0
fi
