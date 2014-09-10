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
import logging

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
  # Initalize the parser
  #
  @staticmethod
  def init_parser (parser):
    download_parser = parser.add_parser ('download',
                                         help = 'Download source files for all projects in the workspace',
                                         description = 'Download source files for all projects in the workspace')

    download_parser.add_argument ('--use-trunk',
                                  help = 'Use the trunk version for projects instead of stable',
                                  action = 'store_true')

    download_parser.set_defaults (cmd = DownloadCommand)

  #
  # Initialize the command object
  #
  def init (self, args):
    self.__use_trunk__ = args.use_trunk
  
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
        logging.getLogger ().info ('downloading {0}...'.format (proj.name ()))
        proj.download (prefix, self.__use_trunk__)
        
        # Update the configuration scripts.
        proj.update_script (prefix, propfile)
        proj.update_script (prefix, script)


