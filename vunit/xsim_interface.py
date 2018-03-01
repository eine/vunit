# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2016, Lars Asplund lars.anders.asplund@gmail.com

"""
Interface for Vivado XSim simulator
"""

from __future__ import print_function
import logging
from os.path import exists, join
import os, shutil
from vunit.ostools import Process
from vunit.simulator_interface import SimulatorInterface
from vunit.exceptions import CompileError
LOGGER = logging.getLogger(__name__)


class XSimInterface(SimulatorInterface):
    """
    Interface for Vivado xsim simulator
    """

    name = "xsim"

    package_users_depend_on_bodies = True

    @classmethod
    def from_args(cls,
                  output_path,  # pylint: disable=unused-argument
                  args):
        """
        Create instance from args namespace
        """
        prefix = cls.find_prefix()
        return cls(prefix=prefix)

    @classmethod
    def find_prefix_from_path(cls):
        """
        Find first valid ghdl toolchain prefix
        """
        return cls.find_toolchain(["xsim"])

    def __init__(self, prefix):
        self._prefix = prefix
        self._libraries = {}

    def setup_library_mapping(self, project):
        """
        Setup library mapping
        """

        for library in project.get_libraries():
            if not exists(library.directory + '\\xsim.dir'):
                os.makedirs(library.directory+ '\\xsim.dir')
            self._libraries[library.name] = library.directory + '\\xsim.dir'

    def compile_source_file_command(self, source_file):
        """
        Returns the command to compile a single source_file
        """
        if source_file.file_type == 'vhdl':
            pass  # TODO
        elif source_file.file_type == 'verilog':
            cmd = [join(self._prefix, 'xvlog.bat'), source_file.name]
            return self.compile_verilog_file_command(source_file, cmd)
        elif source_file.file_type == 'systemverilog':
            cmd = [join(self._prefix, 'xvlog.bat'), '--sv', source_file.name]
            return self.compile_verilog_file_command(source_file, cmd)


        LOGGER.error("Unknown file type: %s", source_file.file_type)
        raise CompileError

    def compile_vhdl_file_command(self, source_file):
        """
        Returns the command to compile a vhdl file
        """
        cmd = [join(self._prefix, 'xvhdl'), source_file.name]
        cmd += ["--work", "%s=%s" % (source_file.library.name, source_file.library.directory)]
        for library_name, library_path in self._libraries.items():
            cmd += ["-L", "%s=%s" % (library_name, library_path)]
        return cmd

    def compile_verilog_file_command(self, source_file, cmd):
        """
        Returns the command to compile a vhdl file
        """
        if (os.path.isdir(source_file.library.directory + '\\xsim.dir') and os.listdir(source_file.library.directory + '\\xsim.dir')):
            pass  # TODO: to get nicer console printout when compiling
            #cmd += ["--work", "%s=%s\\%s" % (source_file.library.name, source_file.library.directory, 'xsim.dir')]
        for library_name, library_path in self._libraries.items():
            if (os.path.isdir(library_path + '\\work') and os.listdir(library_path + '\\work')):
                cmd += ["-L", '"%s=%s\\%s"' % (library_name, library_path, "work")]
        for include_dir in source_file.include_dirs:
            cmd += ["--include", "%s" % include_dir]
        for define_name, define_val in source_file.defines:
            cmd += ["--define", "%s=%s" % (define_name, define_val)]
        return {'cmd' : ' '.join(cmd), 'workdir' : source_file.library.directory}

    def simulate(self,
                 output_path, test_suite_name, config, elaborate_only):
        """
        Simulate with entity as top level using generics
        """

        cmd = [join(self._prefix, 'xelab.bat')]

        for library_name, library_path in self._libraries.items():
            cmd += ["-L", '"%s=%s\\%s"' % (library_name, library_path, "work")]
        cmd += ["--runall"]
        cmd += ["%s.%s" % (config.library_name, config.entity_name)]
        shutil.copytree(os.path.dirname(self._libraries[config.library_name]), output_path)
        for generic_name, generic_value in config.generics.items():
            cmd += ["--generic_top", '"%s=%s"' % (generic_name, generic_value)]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        status = True
        try:
            proc = Process(' '.join(cmd), cwd=output_path)
            proc.consume_output()
        except Process.NonZeroExitCode:
            status = False
        return status
