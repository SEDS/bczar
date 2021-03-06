#!/bin/env python

################################################################################
#
# @file        XscProject.py
#
# $Id: XscProject.py 3691 2012-11-06 20:43:52Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

from ..Project import Project
from ..scm import Git

import os
from os import path
import logging

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return XscProject ()
    
#
# @class XscProject
#
# Implementation of the Project object for XSC.
#
class XscProject (Project):
    __location__ = 'XSC'
    
    #
    # Default constuctor.
    #
    def __init__ (self):
        Project.__init__ (self, 'XSC')

    #
    # Get the project's dependencies. The return value of this
    # function is a list of 1st level project dependencies.
    #
    def get_depends (self):
        return ['DOC', 'MPC']

    #
    # Downlaod the project's source files. The download can be from an online
    # archive, or a source code repository.
    #
    def download (self, ctx):
        abspath = path.abspath (path.join (ctx.prefix, self.__location__))
        url = 'https://github.com/SEDS/XSC.git'
        Git.checkout (url, abspath)

    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self.__location__))
        os.environ['XSC_ROOT'] = abspath

        from ..Utilities import append_libpath_variable
        append_libpath_variable (path.join (abspath, 'lib'))

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        if 'XSC_ROOT' not in os.environ:
            logging.getLogger ().error ('XSC_ROOT environment variable is not defined')
            return False

        return True

    #
    # Update the script with details to configure the environment and
    # support the project.
    #
    # @param[in]            script          ScriptFile object
    #
    def update_script (self, prefix, script):
        abspath = path.abspath (path.join (prefix, self.__location__))

        if path.exists (abspath):
            script_path = script.get_this_variable ()
            location = os.path.join (script_path, self.__location__)

            script.begin_section ('XSC')
            script.write_env_variable ('XSC_ROOT', location)
            script.append_path_variable (path.join (location, 'bin'))
            script.append_libpath_variable (path.join (location, 'lib'))

    #
    # Build the XSC project.
    #
    def build (self, ctx):
        XSC_ROOT = os.environ['XSC_ROOT']
        workspace = path.join (XSC_ROOT, 'XSC.mwc')

        # Generate the workspace
        features = 'xerces3=1,boost=1,exceptions=1'

        if ctx.versioned_namespace:
            features += ',versioned_namespace=1'

        from ..MpcWorkspace import MpcContext, MpcWorkspace
        mpc_ctx = MpcContext (workspace, ctx.build_type, ctx.config, ctx.threads, features, True)
        mwc = MpcWorkspace (mpc_ctx)

        mwc.generate ()
        mwc.build ()

    #
    # Build the XSC project.
    #
    def clean (self, ctx):
        XSC_ROOT = os.environ['XSC_ROOT']
        workspace = path.join (XSC_ROOT, 'XSC.mwc')

        # Generate the workspace
        features = 'xerces3=1,boost=1,exceptions=1'

        if ctx.versioned_namespace:
            features += ',versioned_namespace=1'

        from ..MpcWorkspace import MpcContext, MpcWorkspace
        mpc_ctx = MpcContext (workspace, ctx.build_type, ctx.config, ctx.threads, features, True)
        mwc = MpcWorkspace (mpc_ctx)

        mwc.clean ()
