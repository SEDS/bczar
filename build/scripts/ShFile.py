#!/bin/env python

################################################################################
#
# @file        ScriptFile.py
#
# $Id: ShFile.py 3675 2012-01-06 19:57:22Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

from ..ScriptFile import ScriptFile
from string import Template
import sys
import os

#
# @class ShFile
#
# Wrapper class for generating a .bat file.
#
class ShFile (ScriptFile) :
    #
    # Default constructor.
    #
    def __init__ (self):
        self._file_ = None

    #
    # Write a comment to the batch file
    #
    # @param[in]            comment             Comment string to write
    #
    def write_comment (self, comment):
        self._file_.write ('# ' + comment + '\n')


    #
    # Write a comment section to the batch file
    #
    # @param[in]            name                Name of the section
    #
    def begin_section (self, name):
        tmpl = Template ("""
################################################################################
## ${name}
################################################################################

""")

        params = { 'name' : name }
        self._file_.write (tmpl.substitute (params))

    #
    # Define a new value environment variable.
    #
    # @param[in]            name            Name of environment variable
    # @param[in]            value           Value of environment variable
    #
    def write_env_variable (self, name, value):
        params = { 'name'  : name,
                   'value' : value }

        tmpl = Template ("export ${name}=${value}\n")
        self._file_.write (tmpl.substitute (params))

    #
    # Append value to an existing environment variable.
    #
    # @param[in]            name            Name of environment variable
    # @param[in]            value           Value to append
    #
    def append_env_variable (self, name, value):
        params = { 'name'  : name,
                   'value' : value }

        tmpl = Template ("export ${name}=$${${name}}:${value}\n")
        self._file_.write (tmpl.substitute (params))

    #
    # Write the preamble to the script file. For some subclasses, this
    # will be a no-op. In other cases, this will be a line of text that
    # defines the file type and processor, such as for .sh files.
    #
    def write_preamble (self):
        # Make sure we write the bang!
        self._file_.write ('#!/bin/sh\n')
        self.write_newline ()

        # Pass control to the base class
        ScriptFile.write_preamble (self)

    #
    # Append the value to the PATH environment variable.
    #
    # @param[in]            value           Value to append
    #
    def append_path_variable (self, value):
        self.append_env_variable ('PATH',
                                  os.path.normpath (value))

    #
    # Append the value to the library path environment variable. In Linux
    # environments, this will append the value to LD_LIBRARY_PATH. In MacOS
    # X environments, this will append the value to DYLD_LIBRARY_PATH.
    #
    # @param[in]            value           Value to append
    #
    def append_libpath_variable (self, value):
        if sys.platform == 'darwin':
            self.append_env_variable ('DYLD_LIBRARY_PATH',
                                      os.path.normpath (value))
        else:
            self.append_env_variable ('LD_LIBRARY_PATH',
                                      os.path.normpath (value))
            
    def get_this_variable (self):
        return '$(dirname $(readlink -nf $BASH_SOURCE))'

