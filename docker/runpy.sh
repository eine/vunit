#!/bin/sh

# runpy.sh will execute 'run.py' in $(pwd)
# runpy.sh <path/to/file> will execute <file> in <path/to>

# Get VUNIT_DIR

  # Check if VUnit is installed in the system...
  if [ "$VUNIT_DIR" = "" ] && [ "$(python -c "")" = "" ]; then
    VUNIT_DIR="$(python -c "import vunit;import os;print(os.path.abspath(os.path.dirname(vunit.__file__)))" 2>&1)"
    if [ "$(echo $VUNIT_DIR | grep "No module")" != "" ]; then
      VUNIT_DIR=""
    fi
  fi

  # Check if run.sh resides in a copy of the VUnit repo...
  pysetup="$(dirname $0)/../setup.py"
  if [ "$VUNIT_DIR" = "" ] && [ -f "$pysetup" ] && [ "$(cat "$pysetup" | grep "name='vunit_hdl'")" != ""  ]; then
      VUNIT_DIR="$(cd $(dirname $0)/.. && pwd)"
  fi

  if [ "$VUNIT_DIR" = "" ]; then
    echo "Could not find VUnit installation path. Please set VUNIT_DIR."
    exit 1
  fi

  if [ "$(command -v dos2unix)" != "" ]; then dos2unix "$VUNIT_DIR/bin/ghdl"; fi

# Get script path and name

  pyscript="run.py"

  if [ "$1" != "" ]; then
    cd $(dirname $1)
    pyscript=$(basename $1)
  fi

  if [ ! -f "$pyscript" ]; then
    echo "Error. File $(pwd)/$pyscript not found!"
    exit 1
  fi

# Run

  echo "RUN_DIR: $(pwd)"
  echo "VUNIT_DIR: $VUNIT_DIR"

  $(command -v winpty) docker run --rm -it \
    -v //var/run/docker.sock://var/run/docker.sock \
    -v /$(pwd):/work/src \
    -e VUNIT_RUN_DIR=/$(pwd) \
    -e VUNIT_DIR=/$VUNIT_DIR \
    ghdl/ext:vunit-boot \
    python //work/src/run.py -d "${@:2}"
