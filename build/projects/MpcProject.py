#!/bin/env python

################################################################################
#
# @file        MpcProject.py
#
# $Id: MpcProject.py 3708 2013-04-01 13:55:20Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

from ..Project import Project
from ..scm import Subversion

import os
from os import path

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return MpcProject ()
    
#
# @class MpcProject
#
# Implementation of the Project object for MPC.
#
class MpcProject (Project):
    __location__ = 'MPC'
    
    #
    # Default constuctor.
    #
    def __init__ (self):
        Project.__init__ (self, 'MPC')

    #
    # Downlaod the project's source files. The download can be from an online
    # archive, or a source code repository.
    #
    def download (self, prefix, use_trunk):
        if use_trunk:
            url = 'https://svn.dre.vanderbilt.edu/DOC/MPC/trunk'
        else:
            url = 'https://svn.dre.vanderbilt.edu/DOC/MPC/tags/ACE+TAO+CIAO-6_1_8'
            
        abspath = path.abspath (path.join (prefix, self.__location__))
        Subversion.checkout (url, abspath, 'anonymous', 'anonymous')
        
    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self.__location__))
        os.environ['MPC_ROOT'] = abspath

        append_path_variable (abspath)

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        import subprocess

        if 'MPC_ROOT' not in os.environ:
            print ('*** error: MPC_ROOT environment variable is not defined')
            return False

        subprocess.check_call (["perl", "-v"])
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

            script.begin_section ('MPC')
            script.write_env_variable ('MPC_ROOT', location)
            script.append_path_variable (location)

