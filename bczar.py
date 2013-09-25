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

import getopt
import os
import sys

#
# Display the help screen to the user. This function does not
# return control to the caller. Instead, it exits the system.
#
def print_help (action = None):
    usage = """Setup the environment for building SEM source code

USAGE: bczar.py [OPTIONS] [COMMAND] [COMMAND OPTIONS]

General Options:
  --prefix=PATH                     Target location of sandbox [default=.]
 
  --include=PROJECTS                Comma separated list of projects to include
  --exclude=PROJECTS                Comma separated list of projects to exclude

  --ignore-depends                  Ignore dependency projects during action

Print Options:
  -h, --help [COMMAND]              Print this help information
"""
    # Print the generic help information.
    print (usage)

    commands = get_commands ()

    if action is None:
        # Print a list of supported actions.
        print ('The following is a list of supported commands:')

        for command in commands:
            print ('  %s - %s' % (command.name (), command.description ()))
    else:
        for command in commands:
            if command.name () == action:
                print ('Command Options:')
                command.print_help ()
                break
        
    sys.exit (2)

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
            print ("*** warning: skipping %s; %s not defined" % (module_name, factory))
    
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

    try:
        # Parse the command-line arguments.
        opts, args = getopt.getopt (sys.argv[1:],
                                    'hlp:',
                                    ['help', 'prefix=',
                                     'exclude=', 'include=',
                                     'ignore-depends'])
        
        #
        # @class ScriptOpts
        #
        # Configuration options for the script.
        #
        class ScriptOpts :
            # The default prefix location.
            prefix = '.'
               
            # List of projects to exclude from operation
            excludes = []
            
            # List of projects to include in the operation.
            includes = []
            
            # Ignore the dependency projects
            ignore_depends = False
            
        the_opts = ScriptOpts ()

        for o, a in opts:
            if o == '--prefix':
                the_opts.prefix = a

            elif o in ('-h', '--help'):
                if len (args):
                    print_help (args[0])
                else:
                    print_help ()

            elif o == '--exclude':
                the_opts.excludes.extend (a.split (','))

            elif o == '--include':
                the_opts.includes.extend (a.split (','))
                
            elif o == '--ignore-depends':
                the_opts.ignore_depends = True

        if len (args) == 0:
            print ("*** error: missing command")
            sys.exit (1)
            
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
        commands = get_commands ()
        
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

        # Execute the command on the projects.
        cmdstr = args[0]
        
        for command in commands:
            if cmdstr == command.name ():
                command.init (args[1:])
                command.execute (workspace, the_opts.prefix)
                sys.exit (0)
            
        print ('*** error: <%s> is an unknown command' % cmdstr)
        sys.exit (1)

    except getopt.error as ex:
        print ("*** error: " + ex.args[0])
        sys.exit (1)

#
# Invoke the main entry point, if applicable.
#
if __name__ == "__main__":
    main ()
