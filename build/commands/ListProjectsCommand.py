#!/bin/env python

################################################################################
#
# @file        Command.py
#
# $Id: ListProjectsCommand.py 3661 2011-12-28 22:46:33Z hillj $
#
# @author      James H. Hill
#
################################################################################

from ..Command import Command
from ..Context import Context

#
# Factory method for the command
#
def __create__ ():
  return ListProjectsCommand ()

#
# @class ListProjectsContext
#
class ListProjectsContext (Context):
  @staticmethod
  def init_parser (parser):
    list_parser = parser.add_parser ('list',
                                      help = 'List all projects in the workspace',
                                      description = 'List all projects in the workspace')
    list_parser.set_defaults (cmd = ListProjectsCommand)
    list_parser.set_defaults (ctx = ListProjectsContext)

  def __init__ (self, args):
    Context.__init__ (self, args)

#
# @class ListProjectsCommand
#
# This command will list all the projects in the workspace.
#
class ListProjectsCommand (Command):
  context = ListProjectsContext

  #
  # Get the command's name.
  #
  def name (self):
    return 'list'
  
  #
  # Execute the command
  #
  def execute (self, ctx):
    # List the projects that are known to this script.
    print ("The following is a list of known projects:")
    
    for proj in ctx.workspace.get_projects ():
      print (" . %s" % proj.name ())    
