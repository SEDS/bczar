#!/bin/env python

################################################################################
#
# @file        Command.py
#
# $Id: Command.py 3664 2011-12-29 16:40:54Z hillj $
#
# @author      James H. Hill
#
################################################################################

import getopt

#
# @class Command
#
# Base class for all active commands of the build engine
#
class Command:
    #
    # The name of the command.
    #
    def name (self):
        yield
        
    #
    # A description of the command.
    #
    def description (self):
        return ''
    
    #
    # Initialize the command with the provided arguments.
    #
    def init (self, args):
        pass
    
    #
    # Execute the command. This is called after the command has
    # been initialized.
    #
    def execute (self, workspace, prefix):
        pass
    
    #
    # Print help information about the command.
    #
    def print_help (self):
        pass
    