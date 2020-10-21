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

if [ "$SUBCOMMAND" == "consumer" ]; then
    exec python consumer.py
fi
