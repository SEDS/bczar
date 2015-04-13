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

from ..Command import Command
from ..Context import Context

import os
from os import path
import logging

#
# Factory method for the command
#
def __create__ ():
  return DownloadCommand ()

#
# @class DownloadContext
#
class DownloadContext (Context):
  @staticmethod
  def init_parser (parser):
    download_parser = parser.add_parser ('download',
                                         help = 'Download source files for all projects in the workspace',
                                         description = 'Download source files for all projects in the workspace')

    download_parser.add_argument ('--affiliate',
                                  help = 'Use the private IU github, which requires affiliate access',
                                  action = 'store_true')

    download_parser.add_argument ('--use-trunk',
                                  help = 'Use the trunk version for projects instead of stable',
                                  action = 'store_true')

    download_parser.add_argument ('--use-https',
                                  help = 'Use https:// when downloading via git [default is git://]',
                                  action = 'store_true')

    download_parser.set_defaults (cmd = DownloadCommand)
    download_parser.set_defaults (ctx = DownloadContext)

  def __init__ (self, args):
    Context.__init__ (self, args)
    self.use_trunk = args.use_trunk
    self.use_https = args.use_https
    self.affiliate = args.affiliate

#   
# @class DownloadCommand
#
# Command that downloads all sources in the workspace.
#
class DownloadCommand (Command):
  context = DownloadContext

  #
  # Get the command's name
  #
  def name (self):
    return 'download'
  
  #
  # Execute the command
  #
  def execute (self, ctx):
    # Open the script files where we are going to generate the
    # configuration for the prefix.
    # Open the properties for the file.
    properties_filename = path.join (ctx.prefix, 'configure.properties')
    
    from ..scripts import PropertiesFile
    propfile = PropertiesFile.PropertiesFile ()
    propfile.open (properties_filename)
    
    # Open the script file for writing.
    from .GenerateConfigCommand import open_script_file
    script = open_script_file (ctx.prefix)
    
    for proj in ctx.workspace.order_projects ():
        # Download the project.
        logging.getLogger ().info ('downloading {0}...'.format (proj.name ()))
        proj.download (ctx)
        
        # Update the configuration scripts.
        proj.update_script (ctx.prefix, propfile)
        proj.update_script (ctx.prefix, script)

