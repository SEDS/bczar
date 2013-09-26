#!/bin/env python

################################################################################
#
# @file        CutsProject.py
#
# $Id: MpcWorkspace.py 3709 2013-09-04 15:26:01Z hillj $
#
# @author      James H. Hill
#
################################################################################

import os
from os import path

import subprocess
import sys

#
# @class MpcWorkspace
#
# Wrapper class for using MPC.
#
class MpcWorkspace:
    #
    # Initializing constructor
    #
    # @param[in]          use_ace       Use mwc.pl in $ACE_ROOT/bin
    def __init__ (self, workspace, type, features = None, use_ace = False):
        self._workspace_ = workspace
        self._type_ = type
        self._features_ = features
        self._use_ace_ = use_ace

    #
    # Generate a MPC workspace for a build tool.
    #
    def generate (self):
        env = os.environ

        # Determine the location of mwc.pl
        if self._use_ace_:
            ACE_ROOT = env['ACE_ROOT']
            mwc_pl = path.join (ACE_ROOT, 'bin', 'mwc.pl')

        else:
            MPC_ROOT = env['MPC_ROOT']
            mwc_pl = path.join (MPC_ROOT, 'mwc.pl')

        # Construct the base command line.
        cmd = ['perl', '--', mwc_pl, '-type', self._type_, self._workspace_]

        # Insert the optional features.
        if self._features_ is not None:
            cmd.append ('-features')
            cmd.append (self._features_)

        print (cmd)

        # Execute the workspace generator script
        dir = path.dirname (self._workspace_)
        subprocess.check_call (cmd, cwd = dir)

    #
    # Build the workspace.
    #
    def build (self, config = 'Debug'):
        # Construct the correct build command based on the build type
        if self._type_.find ('vc') == 0:
            # Set the executable command.
            solution = self._workspace_.replace ('.mwc', '.sln')

            from .Utilities import get_vc_executable
            cmd = [get_vc_executable (), solution, '/useenv', '/Build', config]

        elif self._type_ in ('gnuace', 'nmake', 'make'):
            # Set the executable command.
            if self._type_ == 'gnuace':
                if sys.platform == 'darwin':
                    cmd = ['make']
                else:
                    cmd = ['gmake']
            else:
                cmd = [self._type_]

            if self._features_ is not None:
                # Append the macros to the command-line
                macros = self._features_.split (',')

                for macro in macros :
                    cmd.append (macro)

            else:
                print ("*** error: unsupported build type")
                sys.exit (1)

            # Execute the build command
            dir = path.dirname (self._workspace_)
            subprocess.check_call (cmd, cwd = dir)

    #
    # Clean the generated workspace
    #
    def clean (self) :
        # Construct the correct build command based on the build type
        if self._type_.find ('vc') == 0:
            # Set the executable command.
            solution = self._workspace_.replace ('.mwc', '.sln')

            from .Utilities import get_vc_executable
            cmd = [get_vc_executable (), solution, '/useenv', '/Clean', config]

        elif self._type_ in ('gnuace', 'nmake', 'make'):
            # Set the executable command.
            if self._type_ == 'gnuace':
                if sys.platform == 'darwin':
                    cmd = ['make']
                else:
                    cmd = ['gmake']
            else:
                cmd = [self._type_]
        
            # Add the features as macros to the build command.
            if self._features_ is not None :
                for macro in self._features_.split (',') :
                    cmd.append (macro)
            
            # Append the 'realclean' command to the command-line.
            cmd.append ('realclean')

        else:
            print ("*** error: unsupported build type")
            sys.exit (1)

        # Execute the build command
        subprocess.check_call (cmd, cwd = path.dirname (self._workspace_))
        
    #
    # Generate the default features file. The features defined in
    # this file are based on the features provided when this object
    # was created.
    #
    # @param[in]            filename        Name of feature file (optional)
    #
    def generate_default_feature_file (self, filename = 'default.features'):
        feature_file = open (filename, 'w')

        # Write each feature to the file.
        for feature in self._features_.split (','):
            feature_file.write ('%s\n' % feature)

        # Close the file for writing.
        feature_file.close ()

