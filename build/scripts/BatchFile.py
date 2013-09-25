#!/bin/env python

################################################################################
#
# @file        BatchFile.py
#
# $Id: BatchFile.py 3668 2011-12-31 05:33:47Z hillj $
#
# @author      James H. Hill
#
################################################################################

import os

from ..ScriptFile import ScriptFile
from string import Template

#
# @class BatchFile
#
# Wrapper class for generating a .bat file.
#
class BatchFile (ScriptFile) :
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
    self._file_.write ('@rem ' + comment + '\n')

  #
  # Write a comment section to the batch file
  #
  # @param[in]            name                Name of the section
  #
  def begin_section (self, name):
    tmpl = Template ("""
@rem ***************************************************************************
@rem ** ${name}
@rem ***************************************************************************

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
    params = { 'name'   : name,
                'value' : value }

    tmpl = Template ("@set ${name}=${value}\n")
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

    tmpl = Template ("@set ${name}=%${name}%;${value}\n")
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
    self.append_path_variable (value)
    
  #
  # Get the script relative location macro.
  #
  def get_this_variable (self):
    return '%~dp0'
