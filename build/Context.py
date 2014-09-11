#!/bin/env python

import argparse
import os

#
# @class Context
#
# Class which aggregates Contextual information about the command,
# namely, the command line arguments which modify the behavior of the commands
class Context:
  @staticmethod
  def init_parser (parser):
    parser.add_argument ('--prefix', '-p',
                         help = 'Target location of sandbox [default=.]',
                         default = os.path.curdir,
                         metavar = 'PATH',
                         type = str)

    parser.add_argument ('--includes', '-i',
                         help = 'Comma separated list of projects to include',
                         metavar = 'PROJECTS',
                         type = str)

    parser.add_argument ('--excludes', '-e',
                         help = 'Comma separated list of projects to exclude',
                         metavar = 'PROJECTS',
                         type = str)

    parser.add_argument ('--ignore-depends',
                         help = 'Ignore dependency projects during action',
                         action = 'store_true')
 
  def __init__ (self, args):
    if args.includes:
      self.includes = args.includes.split (',')
    else:
      self.includes = []

    if args.excludes:
      self.excludes = args.excludes.split (',')
    else:
      self.excludes = []

    self.ignore_depends = args.ignore_depends
    self.prefix = args.prefix
    self.workspace = None
