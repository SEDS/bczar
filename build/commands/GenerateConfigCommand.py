#!/bin/env python

################################################################################
#
# @file        GenerateConfigCommand.py
#
# $Id: GenerateConfigCommand.py 3661 2011-12-28 22:46:33Z hillj $
#
# @author      James H. Hill
#
################################################################################

from ..Command import Command

import os
from os import path

#
# Factory method for the command
#
def __create__ ():
  return GenerateConfigCommand ()
  
#   
# @class GenerateConfigCommand
#
# Command that generates the configuration files for a workspace.
#
class GenerateConfigCommand (Command):  
  #
  # Get the command's name
  #
  def name (self):
    return 'genconfig'

  #
  # Get the commands description
  # 
  def description (self):
    return "Generate the workspace's configuration file"

  #
  # Execute the command
  #
  def execute (self, workspace, prefix):
    # Open the properties for the file.
    properties_filename = path.join (prefix, 'configure.properties')
    
    from ..scripts import PropertiesFile
    propfile = PropertiesFile.PropertiesFile ()
    propfile.open (properties_filename)
    
    # Open the script file for writing.
    script = open_script_file (prefix)
    
    for proj in workspace.get_projects ():
      print ('*** info: updating script for %s...' % proj.name ())
      proj.update_script (prefix, propfile)
      proj.update_script (prefix, script)  

#
# Helper method that open the script file for the correct
# platform. This is important since different platforms have
# different ways of configuring their environment from the
# command-line.
#
def open_script_file (prefix):
  from ..Utilities import is_windows_platform
  
  if is_windows_platform ():
    # We are going to use a batch file.
    from build.scripts import BatchFile
    script = BatchFile.BatchFile ()        
    script.open (path.join (prefix, 'configure.bat'))
    
  else:
    from build.scripts import ShFile
    script = ShFile.ShFile ()
    script.open (path.join (prefix, 'configure.sh'))
      
  return script