#!/bin/env python

################################################################################
#
# @file        PropertiesFiles.py
#
# $Id: PropertiesFile.py 3671 2012-01-02 15:41:46Z hillj $
#
# @author      James H. Hill
#
################################################################################

import os
import sys

from ..ScriptFile import ScriptFile
from string import Template

#
# @class PropertiesFile
#
# Wrapper class for generating a .bat file.
#
class PropertiesFile (ScriptFile) :
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
                   'value' : os.path.normpath (value) }

        tmpl = Template ("${name}=${value}\n")
        self._file_.write (tmpl.substitute (params))

    #
    # Read the contents of a property file
    #
    # @param[in]            filename          Name of the property file
    # @return               Dictionary object
    #
    def read (filename):
        file = open (filename, 'r')
        props = {'SCRIPT_PATH' : os.path.abspath (os.path.dirname (filename)),
                 'LIB_PATH' : '',
                 'PATH' : ''}
         
        for line in file:
            line = line.strip ()
    
            if len (line) > 0 and line[0] != '#':
              # This not a comment line. So, we need to split the contents of
              # the line by the equal sign.
              if '$' in line:
                template = Template (line)
                line = template.substitute (props)
              
              entry = line.split ('=', 1)
    
              # Let's assume the value is a path, and that we need to normalize
              # its contents.
              props[entry[0]] = os.path.normpath (entry[1])

        return props

    #
    # Append value to an existing environment variable.
    #
    # @param[in]            name            Name of environment variable
    # @param[in]            value           Value to append
    #
    def append_env_variable (self, name, value):
        params = {  'name'  : name,
                    'value' : value }
  
        if sys.platform.startswith ('win32'):
            tmpl = Template ('${name}=$${${name}};${value}\n')
        else:
            tmpl = Template ('${name}=$${${name}}:${value}\n')

        self._file_.write (tmpl.substitute (params))

    #
    # Append the value to the PATH environment variable.
    #
    # @param[in]            value           Value to append
    #
    def append_path_variable (self, value):
      self.append_env_variable ('PATH', os.path.normpath (value))
  
    #
    # Append the value to the library path environment variable. This
    # will append the value to the PATH variable as well.
    #
    # @param[in]            value           Value to append
    #
    def append_libpath_variable (self, value):
      self.append_env_variable ('LIB_PATH', os.path.normpath (value))

    #
    # Get the variable that points to the location of the script
    # that is executing. This helps with sandboxing the source files
    # that are downloaded via the build engine.
    #
    def get_this_variable (self):
      return '${SCRIPT_PATH}'
