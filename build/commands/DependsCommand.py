#!/bin/env python

################################################################################
#
# @file        DependsCommand.py
#
# $Id: DependsCommand.py 3661 2011-12-28 22:46:33Z hillj $
#
# @author      James H. Hill
#
################################################################################

from ..Command import Command

#
# Factory method for the command object
#
def __create__ ():
  return DependsCommand ()
  
#
# @class  DependsCommand
#
# Command that list the dependencies of all projects in the workspace.
#
class DependsCommand (Command):
  def name (self):
    return 'depends' 

  #
  # Initalize the parser
  #
  @staticmethod
  def init_parser (parser):
    depends_parser = parser.add_parser ('depends',
                                        help = 'List dependencies for all projects in the workspace',
                                        description = 'List dependencies for all projects in the workspace')

    depends_parser.set_defaults (cmd = DependsCommand)

  #
  # Execute the command
  #
  def execute (self, workspace, prefix):
    for proj in workspace.get_projects ():
      print ('')
      print ('%s Dependencies' % proj.name ())
      print ('======================================')
        
      for depend in workspace.get_depends (proj.name ()):
        print ('.', depend.name ()) 
