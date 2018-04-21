This article is focused on a modularized approach to execute VUnit with multiple docker containers. If you are looking for a straightforward solution to run VUnit in a single container (including python, package dependencies, VUnit and a simulator), see [Continuous Integration (CI) Environment](https://vunit.github.io/cli.html?highlight=continuous#continuous-integration-ci-environment).

NOTE: this feature is not merged into the main branch of VUnit, and it is not supported. See [VUnit/vunit#324](https://github.com/VUnit/vunit/issues/324).

---

# Usage

Steps to adapt an existing project and use the modularized container approach:

- Copy `VUnit_docker.py` to the same folder as `run.py`.
- Edit `run.py` to replace `from vunit import VUnit` with `from VUnit_docker import VUnit`.
- Add arg `-d` or `--docker` when you execute `run.py`.
  - Ensure that script `bin/ghdl` in the VUnit installation has GNU/Linux line-endings.

Note that all the path strings used in the tests must use the paths inside the containers, and not the absolute paths in the host. By default, two directories are shared between the host and the containers:

- `/work/run`: the project directory, which is the one where `run.py` is located. The ouputs are generated in `/work/run/vunit_out`.
- `/work/vunit`: directory with VUnit sources. If VUnit is not installed in the host system, envvar `VUNIT_DIR` must be set to the path of the sources prior to executing `run.py`.

Optionally, argument `vols` can be provided to `VUnit.from_argv`, in order to describe additional paths that need to be bind. The format is the one expected by the docker package (see [Docker SDK for Python: Containers](https://docker-py.readthedocs.io/en/stable/containers.html)):

> volumes (dict or list) – A dictionary to configure volumes mounted inside the container. The key is either the host path or a volume name, and the value is a dictionary with the keys:
>    
> bind The path to mount the volume inside the container mode Either rw to mount the volume read/write, or ro to mount it read-only.

For example:

```
  {
    '/home/user/data': {'bind': '/work/data', 'mode': 'rw'},
    '/opt/tools': {'bind': '/work/tools', 'mode': 'ro'}
  }
```

As explained in the docs, these can also be docker volume names, which can be useful in Swarm environments.

# Dependency-free script

Script `docker/runpy.sh` is provided to help users execute tests in hosts with no installed dependencies but docker. Prepend `runpy.sh` to the execution command, e.g. `runpy.sh run.py -d -v`, in order to have it executed inside a container. This script will automatically get the default dir paths for you.

# Execution flow

## Without `runpy.sh`

When the VUnit execution script is run natively with the docker flag, two containers are executed in the background:

- `vunit-sim`: any container with GHDL installed and available in the PATH. Defaults to `ghdl/ghdl:ubuntu18-llvm-5.0`, and can be overriden with envvar `VUNIT_SIM_IMG`.
- `vunit-run`: any container with Python (including packages colorama and docker) and Docker CLI. Defaults to `vunit/boot:3.6-alpine`, and can be overriden with envvar `VUNIT_RUN_IMG`.

Both containers share the same paths with the host. On top of that, the docker unix socket of the host is bind to `vunit-run`.

Then, the run script is executed inside `vunit-run` with a modified `sys.path` and with all the flags except `-d`. This modification of the path adds `/work/vunit/bin`, in order to let VUnit find a fake executable.

As a result, when the simulator/compiler is called, the fake executable in `/work/vunit/bin` executes a `docker exec` command that forwards the order to `vunit-sim`.

When the run script exists, both containers are removed.

## With `runpy.sh`

If python is not available in the host, `runpy.sh` first runs a temporal container with the docker socket bind. This container has the same requirements as `vunit-run`, but a single bind volume (the path of the run script). Inside, the run script is executed and two containers are created, as explained above.

# TODO

- [ ] `VUnit_docker.py:30`:  this fails if vunit is installed in a system without any valid simulator. How to get the vunit install path in such context?
- [ ] `VUnit_docker.py:144`: extract the content from the Error object and decode it with `.decode('UTF-8')`
