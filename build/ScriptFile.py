#!/bin/env python

################################################################################
#
# @file        ScriptFile.py
#
# $Id: ScriptFile.py 3668 2011-12-31 05:33:47Z hillj $
#
# @author      James H. Hill
#
################################################################################

#
# @class ScriptFile
#
# Base class for all scripting files. It defines the default operations
# that are common to all scripting file types, such as .bat, .sh, and
# .properties file.
#
class ScriptFile:
  #
  # Default constructor.
  #
  def __init__ (self, comment_tmpl):
    self._file_ = None
    self._comment_tmpl_ = comment_tmpl

  #
  # Open the file for writing.
  #
  # @param[in]            filename            Name of file to open
  #
  def open (self, filename):
    self._file_ = open (filename, "w")

  #
  # Close the batch file
  #
  def close (self):
    self._file_.close ()
    self._file_ = None

  #
  # Test if the current file is open.
  #
  def is_open (self):
    return self._file_ is not None;

  #
  # Write a new line to the script.
  #
  def write_newline (self):
    self._file_.write ('\n')

  #
  # Write the preamble to the script file. For some subclasses, this
  # will be a no-op. In other cases, this will be a line of text that
  # defines the file type and processor, such as for .sh files.
  #
  def write_preamble (self):
    self.write_comment ('This file was generated:')
    self.write_comment (",".join (sys.argv).replace (",", " "))

  #
  # Write a new section to the script. This should write the section
  # name within a formatted comment.
  #
  # @param[in]            name            Name of new section.
  #
  def begin_section (self, name):
    pass

  #
  # Write a new comment.
  #
  # @param[in]            comment         The actual comment.
  #
  def write_comment (self, comment):
    pass

  #
  # Define a new value environment variable.
  #
  # @param[in]            name            Name of environment variable
  # @param[in]            value           Value of environment variable
  #
  def write_env_variable (self, name, value):
    pass

  #
  # Append value to an existing environment variable.
  #
  # @param[in]            name            Name of environment variable
  # @param[in]            value           Value to append
  #
  def append_env_variable (self, name, value):
    pass

  #
  # Append the value to the PATH environment variable.
  #
  # @param[in]            value           Value to append
  #
  def append_path_variable (self, value):
    pass

  #
  # Append the value to the library path environment variable. Depending
  # on the platform, the target variable will differ.
  #
  # @param[in]            value           Value to append
  #
  def append_libpath_variable (self, value):
    pass

  #
  # Get the variable that points to the location of the script
  # that is executing. This helps with sandboxing the source files
  # that are downloaded via the build engine.
  #
  def get_this_variable (self):
    return ''