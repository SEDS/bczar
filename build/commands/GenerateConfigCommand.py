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
from ..Context import Context

import os
from os import path
import logging


#
# Factory method for the command
#
def __create__():
  return GenerateConfigCommand()


#
# @class GenerateConfigContext
#
class GenerateConfigContext(Context):
  @staticmethod
  def init_parser(parser):
    genconfig_parser = parser.add_parser('genconfig',
                                         help='Generate the workspace\'s configuration file',
                                         description='Generate the workspace\'s configuration file')
    genconfig_parser.set_defaults(cmd=GenerateConfigCommand)
    genconfig_parser.set_defaults(ctx=GenerateConfigContext)

  def __init__(self, args):
    Context.__init__(self, args)


#
# @class GenerateConfigCommand
#
# Command that generates the configuration files for a workspace.
#
class GenerateConfigCommand(Command):
  context = GenerateConfigContext

  #
  # Get the command's name
  #
  def name(self):
    return 'genconfig'

  #
  # Execute the command
  #
  def execute(self, ctx):
    # Open the properties for the file.
    properties_filename = path.join(ctx.prefix, 'configure.properties')

    from ..scripts import PropertiesFile
    propfile = PropertiesFile.PropertiesFile()
    propfile.open(properties_filename)

    # Open the script file for writing.
    from ..ScriptFile import open_script
    script = open_script (ctx.prefix)
    script.write_preamble ()

    for proj in ctx.workspace.get_projects():
      logging.getLogger().info('updating script for {0}...'.format(proj.name()))
      proj.update_script(ctx.prefix, propfile)
      proj.update_script(ctx.prefix, script)
