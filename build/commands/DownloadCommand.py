#!/bin/env python

################################################################################
#
# @file        DownloadCommand.py
#
# $Id: DownloadCommand.py 3681 2012-05-03 19:17:32Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

import getopt
from ..Command import Command

import os
from os import path

#
# Factory method for the command
#
def __create__ ():
  return DownloadCommand ()
  
#   
# @class DownloadCommand
#
# Command that downloads all sources in the workspace.
#
class DownloadCommand (Command):
  __use_trunk__= False
  __username__ = None
  __password__ = None
  
  #
  # Get the command's name
  #
  def name (self):
    return 'download'
  
  #
  # Get the commands description
  # 
  def description (self):
    return "Download source files for all projects in the workspace"

  #
  # Initialize the command object
  #
  def init (self, args):
    # Parse the command-line arguments.
    long_options = ['trunk']
    opts, args = getopt.getopt (args, '', long_options)
    
    for o, a in opts:
      if o == '--trunk':
        self.__use_trunk__ = True
  
  #
  # Execute the command
  #
  def execute (self, workspace, prefix):
    # Open the script files where we are going to generate the
    # configuration for the prefix.
    # Open the properties for the file.
    properties_filename = path.join (prefix, 'configure.properties')
    
    from ..scripts import PropertiesFile
    propfile = PropertiesFile.PropertiesFile ()
    propfile.open (properties_filename)
    
    # Open the script file for writing.
    from .GenerateConfigCommand import open_script_file
    script = open_script_file (prefix)
    
    for proj in workspace.order_projects ():
        # Download the project.
        print ('*** info: downloading %s...' % proj.name ())
        proj.download (prefix, self.__use_trunk__)
        
        # Update the configuration scripts.
        proj.update_script (prefix, propfile)
        proj.update_script (prefix, script)
        
  #
  # Print command help information
  #
  def print_help (self):
    usage = """  --trunk                           Download trunk version(s)
"""
    print (usage)
