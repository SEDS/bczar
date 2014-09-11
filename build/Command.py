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
    # Context to use for the Command, this should be the class name.
    context = None

    #
    # The name of the command.
    #
    def name (self):
        yield

    #
    # Execute the command. This is called after the context has
    # been initialized.
    #
    def execute (self, context):
        pass
