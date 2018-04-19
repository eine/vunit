#!/bin/sh

# VUNIT_DIR
# PROJECT_DIR
# VUNIT_SIMULATOR_DOCKER_IMG

set -e

# Get VUNIT_DIR

if [ "$VUNIT_DIR" = "" ] && [ "$(python -c "")" = "" ]; then
  export VUNIT_DIR="$(python -c "import vunit;import os;print(os.path.abspath(os.path.dirname(vunit.__file__)))" 2>&1)"
  if [ "$( echo $VUNIT_DIR | grep "No module")" = "" ]; then
    export VUNIT_DIR=""
  fi
fi

if [ "$VUNIT_DIR" = "" ] && [ -f "$(dirname $0)/setup.py" ] && [ "$(cat setup.py | grep "name='vunit_hdl'")" != ""  ]; then
    export VUNIT_DIR="$(pwd)"
fi

if [ "$VUNIT_DIR" = "" ]; then
  echo "Could not find VUnit installation path. Please set VUNIT_DIR."
  exit 1
fi

# Get PROJECT_DIR

if [ "$PROJECT_DIR" = "" ]; then
  if [ "$1" != "" ]; then
    export PROJECT_DIR="$(cd $(dirname $1) && pwd)"
  else
    export PROJECT_DIR="$(pwd)"
  fi
fi

# Setup docker container

if [ "$VUNIT_SIMULATOR_DOCKER_IMG" = "" ]; then
  export VUNIT_SIMULATOR_DOCKER_IMG="ghdl/ghdl:stretch-mcode"
fi

docker run --name vunit-sim -d \
  -v "/${PROJECT_DIR}://src" \
  -v "/${VUNIT_DIR}://vunit" \
  "${VUNIT_SIMULATOR_DOCKER_IMG}" \
  tail -f /dev/null

# Setup Python

if [ "$PYTHONPATH" = "" ]; then
  export PYTHONPATH="$VUNIT_DIR"
else
  export PYTHONPATH="${PYTHONPATH}:{$VUNIT_DIR}"
fi

# Setup VUnit

export VUNIT_SIMULATOR="ghdl"
export VUNIT_GHDL_PATH="$VUNIT_DIR/bin"

set +e

# Run project

cd "$PROJECT_DIR"
pyscript="$(basename $1)"
shift
python "$pyscript" $@
exitcode=$?

# Docker teardown

docker logs vunit-sim
docker rm -f vunit-sim

exit $exitcode
