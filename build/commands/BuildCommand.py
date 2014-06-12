#!/bin/env python

################################################################################
#
# @file        BuildCommand.py
#
# $Id: BuildCommand.py 3699 2012-12-18 19:08:52Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

import getopt
import os
import sys

from ..Command import Command

#
# Factory method for the command
#
def __create__ ():
  return BuildCommand ()
  
#   
# @class BuildCommand
#
# Command that builds all projects in the workspace.
#
class BuildCommand (Command):
  __versioned_namespace__ = False
  __clean__ = False
  
  #
  # Get the command's name
  #
  def name (self):
    return 'build'
  
  #
  # Get the command's description
  #
  def description (self):
    return 'Build all projects in the workspace'

  #
  # Initialize the command object
  #
  def init (self, args):
    # Parse the command-line arguments.
    long_options = ['versioned-namespace', 'clean']
    opts, args = getopt.getopt (args, '', long_options)
    
    for o, a in opts:
        if o == "--versioned-namespace":
          self.__versioned_namespace__ = True
        elif o == '--clean':
          self.__clean__ = True
  
  #
  # Execute the command
  #
  def execute (self, workspace, prefix):
    # First, configure the environment so the build does not fail
    # because of missing environment variables.
    configure_environment (prefix)
    
    # Auto-detect the build type.
    from ..Utilities import autodetect_build_type
    build_type = autodetect_build_type ()

    # Validate build environment
    print ('*** info: validating build environment')
    for proj in workspace.order_projects ():
        if not proj.validate_environment ():
            sys.exit (1)
    
    if (self.__versioned_namespace__):
        print ('*** info: building projects with versioned namespace support')
        
    if (self.__clean__):
      for proj in workspace.order_projects ():
          print ('*** info: cleaning %s...' % proj.name ())
          proj.clean (prefix, build_type, self.__versioned_namespace__)
    else:
      for proj in workspace.order_projects ():
          print ('*** info: building %s...' % proj.name ())
          proj.build (prefix, build_type, self.__versioned_namespace__)
      
  #
  # Print command help information
  #
  def print_help (self):
    usage = """  --versioned-namespace             Build with versioned namespace support
  --clean                           Clean the projects               
"""

    print (usage)


#
# Utility method that configures the enviroment using the properties
# file at the specified location
#
# @param          prefix          Location of property file 
#
def configure_environment (prefix):
  print ("*** info: configuring the enviroment")
  # Load the existing properties file into memory and use it
  # to configure our execution environment, if the file does
  # indeed exist.
  properties_filename = os.path.join (prefix, 'configure.properties')

  if os.path.exists (properties_filename):
      # Read the properties from the file, and update the
      # environment variables.
      print ('*** info: loading properties from %s' % properties_filename)

      from ..scripts import PropertiesFile
      props = PropertiesFile.PropertiesFile.read (properties_filename)

      for key, value in props.items ():
          if key == 'LIB_PATH':
              from build.Utilities import append_libpath_variable
              append_libpath_variable (value)
          elif key == 'PATH':
              from build.Utilities import append_path_variable
              append_path_variable (value)                
          else:
              os.environ[key] = value
  else:
      print ('*** error: %s does not exist' % properties_filename)


