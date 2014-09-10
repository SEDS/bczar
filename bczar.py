#!/usr/bin/env python

###############################################################################
#
# @file        bczar.py
#
# $Id: bczar.py 3687 2012-10-12 22:20:24Z hillj $
#
# @author      James H. Hill
#
###############################################################################

import os
import sys
import argparse
import logging

#
# Factory method to create a commandline parser
# returns an argparse.ArgumentParser
#
def create_parser ():
    # create the common parser
    top_level_parser = argparse.ArgumentParser ()
    top_level_parser.add_argument ('--prefix', '-p',
                                   help = 'Target location of sandbox [default=.]',
                                   default = os.path.curdir,
                                   metavar = 'PATH',
                                   type = str)

    top_level_parser.add_argument ('--includes', '-i',
                                   help = 'Comma separated list of projects to include',
                                   metavar = 'PROJECTS',
                                   type = str)

    top_level_parser.add_argument ('--excludes', '-e',
                                   help = 'Comma separated list of projects to exclude',
                                   metavar = 'PROJECTS',
                                   type = str)

    top_level_parser.add_argument ('--ignore-depends',
                                   help = 'Ignore dependency projects during action',
                                   action = 'store_true')

    subparsers = top_level_parser.add_subparsers (help = 'sub-command help')

    for command in get_commands ():
        command.init_parser (subparsers)

    return top_level_parser

#
# Dynamically import objects located on disk
#
# @param            path                Location of objects
# @param            factory             Factory method to create object
#
def import_objects (prefix, imports, factory):
    objects = []
    
    # Evaluate each of the installed pre-commit hooks.
    
    for name in os.listdir (os.path.join (prefix, imports)):
      if name.endswith (".py") and name != '__init__.py':
        # Helper method that extracts the modules name from the provided
        # Python script name.
        def get_module_basename (script):
          return script[0:len (script) - 3]
        
        # Import the __create__ function for the project module.
        module_basename = get_module_basename (name)
        module_name = imports.replace ('/', '.') + '.' + module_basename
        hook = __import__ (module_name, globals (), locals (), [factory])
        
        if factory in dir (hook):
            eval_str = 'hook.%s ()' % factory
            objects.append (eval (eval_str))
        else:
            logging.getLogger ().warning ('skipping {0}; {1} not defined'.format (module_name, factory))
    
    return objects

#
# Helper method that imports all the command objects
#
def get_commands ():
    script_path = os.path.dirname (sys.argv[0])       
    return import_objects (script_path, 'build/commands', '__create__')
    
#
# Helper method that imports all the project objects
#
def get_projects ():
    script_path = os.path.dirname (sys.argv[0])       
    return import_objects (script_path, 'build/projects', '__create__')
    
#
# Main entry point for the application.
#
def main ():
    # Check that python version is 3.0 or higher
    if sys.version_info < (3,0):
            print ("*** error: Python 3 is required")
            sys.exit (1)

    # setup the logging format
    logging.basicConfig (format='*** %(levelname)s: %(message)s', level = logging.INFO)

    try:
        # Parse the command-line arguments.
        parser = create_parser ()
        the_opts = parser.parse_args ()

        # split the list of includes/excludes
        if the_opts.includes is not None:
            the_opts.includes = the_opts.includes.split(',')
        else:
            the_opts.includes = []

        if the_opts.excludes is not None:
            the_opts.excludes = the_opts.excludes.split(',')
        else:
            the_opts.excludes = []

        # uncomment to see the options printed (e.g. 'Namespace(...)')
        logging.getLogger ().debug ('Script options:\n\t{0}'.format (the_opts))

        #
        # Test if a project is enabled. The project is enabled it appears
        # in the includes listing, or it does not appear in the excludes
        # listing. If the includes listing is empty, then the project is
        # enabled if it does not appear in the excludes listing.
        #
        def is_enabled (proj, ignore_includes = False):
            if not ignore_includes and len (the_opts.includes) > 0:
                return proj.name () in the_opts.includes
            else:
                return not proj.name () in the_opts.excludes
            
        # Get all the projects we know about. Regardless of what operation
        # we complete below, we need a list of all projects. Now, the list
        # will be based on those specified in the includes, and not specified
        # in the excludes section. For those project that are enabled, we
        # are going to add them to a workspace.
        projects = get_projects ()
        
        from build.Workspace import Workspace
        
        if len (the_opts.includes) or len (the_opts.excludes):
            # Create an empty workspace.
            workspace = Workspace ()
            full_workspace = Workspace (projects)

            # Only add projects to the workspace that should be
            # actually included in it.
            for proj in projects:
                if is_enabled (proj):
                    # Insert the project into the workspace.
                    workspace.insert (proj)
                    
                    if not the_opts.ignore_depends:
                        # Insert the project's dependencies into the workspace.
                        for depend in full_workspace.get_depends (proj.name ()):
                            if is_enabled (depend, True):
                                workspace.insert (depend)

        else:
            # Create a workspace from all projects.
            workspace = Workspace (projects)

        # Make the prefix directory just in case it does not
        # exist at the moment.
        if not os.path.exists (the_opts.prefix):
            os.makedirs (the_opts.prefix)

        # Execute the command on the workspace.
        command = the_opts.cmd ()
        command.init (the_opts)
        command.execute (workspace, the_opts.prefix)

    except Exception as ex:
        logging.getLogger ().error (ex)
        sys.exit (1)

#
# Invoke the main entry point, if applicable.
#
if __name__ == "__main__":
    main ()
