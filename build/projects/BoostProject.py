#!/bin/env python

################################################################################
#
# @file        BoostProject.py
#
# $I`d: bczar.py 3656 2011-11-29 16:43:50Z hillj $
#
# @author      James H. Hill
#
################################################################################

import os
import sys

from ..Project import Project
from ..scm import Subversion
from os import path

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return BoostProject ()

#
# @class BoostProject
#
# Implementation of the Project class for Xerces-C.
#
class BoostProject (Project):
    __location__ = 'boost'

    #
    # Default constructor
    #
    def __init__ (self):
        Project.__init__ (self, 'Boost')

    #
    # Download the Boost source files. The source files are taken from
    # trunk in the SVN repo.
    #
    def download (self, prefix, use_trunk):
        # XSC requires boost filesystem version 2.  1.49 is the last release
        # to include filesystem version 2.  It is also the first release to support
        # vc11.
        url = 'https://svn.boost.org/svn/boost/tags/release/Boost_1_49_0'
        abspath = path.abspath (path.join (prefix, self.__location__))
        Subversion.checkout (url, abspath)

    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self._location_))

        # Update the environment variables.
        os.environ['BOOST_ROOT'] = abspath

        if sys.platform == 'win32':
            os.environ['BOOST_VERSION'] = 'boost-1_49'

        append_libpath_variable (path.join (abspath, 'lib'))

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        if 'BOOST_ROOT' not in os.environ:
            print ('*** error: BOOST_ROOT environment variable is not defined')
            return False

        if sys.platform == 'win32' and 'BOOST_VERSION' not in os.environ:
            print ('*** error: BOOST_VERSION environment variable is not defined')
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

            script.begin_section ('Boost')
            script.write_env_variable ('BOOST_ROOT', location)

            # Locate the Boost version in the version source file. We are
            # going to use it to set the BOOST_VERSION environment variable.
            version_filename = path.join (abspath, 'boost', 'version.hpp')
            version_file = open (version_filename, 'r')

            for line in version_file:
                if '#define' in line and 'BOOST_LIB_VERSION' in line:
                    BOOST_VERSION = line.replace ('"', '').split ()[2]
                    break

            version_file.close ()

            script.write_env_variable ('BOOST_VERSION', BOOST_VERSION)
            script.append_libpath_variable (path.join (location, 'lib'))

    #
    # Build the project
    #
    def build (self, prefix, type, versioned_namespace):
        import subprocess

        BOOST_ROOT = os.environ['BOOST_ROOT']
        project_config = path.join (BOOST_ROOT, 'project-config.jam')
        prefix_arg = '--prefix=' + BOOST_ROOT

        if not path.exists (project_config):
            # First, we need to boostrap the Boost environment.
            if sys.platform == 'win32':
              bootstrap = path.join (BOOST_ROOT, 'bootstrap.bat')
            else:
              bootstrap = path.join (BOOST_ROOT, 'bootstrap.sh')

            cmd = [bootstrap, prefix_arg]
            subprocess.check_call (cmd, cwd = BOOST_ROOT)

        # Now, we can actually build Boost using the local version of bjam
        bjam = path.join (BOOST_ROOT, 'bjam')
        if sys.platform == 'win32':
            toolsets = { 'vc71'     : 'msvc-7.1',
                         'vc8'      : 'msvc-8.0',
                         'vc9'      : 'msvc-9.0',
                         'vc10'     : 'msvc-10.0',
                         'vc11'     : 'msvc-11.0'}

            cmd = [bjam,
                   prefix_arg,
                   '--build-type=complete',
                   '--layout=versioned',
                   '--without-python',
                   '--without-math',
                   '--without-signals',
                   '--toolset=' + toolsets[type],
                   '--abbreviate-paths',
                   'install']

        else:
          cmd = [bjam, prefix_arg, '--without-python', 'install', '-sNO_COMPRESSION=1']

        subprocess.check_call (cmd, cwd = BOOST_ROOT)