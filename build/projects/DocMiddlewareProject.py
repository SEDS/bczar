#!/bin/env python

################################################################################
#
# @file        DocMiddlewareProject.py
#
# $Id: DocMiddlewareProject.py 3709 2013-09-04 15:26:01Z hillj $
#
# @author      James H. Hill
#
################################################################################

from ..Project import Project
from ..scm import Subversion

import os
from os import path
import subprocess
import logging

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return DocMiddlewareProject ()

#
# @class DocMiddlewareProject
#
# Implemenation of the Project object for building the DOC
# middleware source code.
#
class DocMiddlewareProject (Project):
    __location__ = 'Middleware'

    #
    # Default constructor.
    #
    def __init__ (self):
        Project.__init__ (self, 'DOC')

    #
    # Get the project's dependencies. The return value of this
    # function is a list of 1st level project dependencies.
    #
    def get_depends (self):
        return ['Boost', 'MPC', 'XercesC']

    #
    # Downlaod the project's source files. The download can be from an online
    # archive, or a source code repository.
    #
    def download (self, ctx):
        if ctx.use_trunk:
            url = 'https://svn.dre.vanderbilt.edu/DOC/Middleware/trunk'
        else:
            url = 'https://svn.dre.vanderbilt.edu/DOC/Middleware/tags/ACE+TAO+CIAO-6_1_8'

        abspath = path.abspath (path.join (ctx.prefix, self.__location__))
        Subversion.checkout (url, abspath, 'anonymous', 'anonymous')

    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self.__location__))

        os.environ['ACE_ROOT'] = path.join (abspath, 'ACE')
        os.environ['TAO_ROOT'] = path.join (abspath, 'TAO')
        os.environ['CIAO_ROOT'] = path.join (abspath, 'CIAO')
        os.environ['DANCE_ROOT'] = path.join (abspath, 'DAnCE')

        append_path_variable (path.join (abspath, 'ACE', 'bin'))
        append_path_variable (path.join (abspath, 'CIAO', 'bin'))
        append_path_variable (path.join (abspath, 'DAnCE', 'bin'))

        append_libpath_variable (path.join (abspath, 'ACE', 'lib'))
        append_libpath_variable (path.join (abspath, 'DAnCE', 'lib'))

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        if ('ACE_ROOT' not in os.environ) or \
           ('TAO_ROOT' not in os.environ) or \
           ('CIAO_ROOT' not in os.environ) or \
           ('DANCE_ROOT' not in os.environ):
            logging.getLogger ().error ('DOC middleware environment variable(s) are not defined')
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

            script.begin_section ('Middleware')
            script.write_env_variable ('ACE_ROOT', path.join (location, 'ACE'))
            script.write_env_variable ('TAO_ROOT', path.join (location, 'TAO'))
            script.write_env_variable ('CIAO_ROOT', path.join (location, 'CIAO'))
            script.write_env_variable ('DANCE_ROOT', path.join (location, 'DAnCE'))

            script.write_newline ()

            script.write_comment ('Define the location of the binaries')
            script.append_path_variable (path.join (location, 'ACE/bin'))
            script.append_path_variable (path.join (location, 'CIAO/bin'))
            script.append_path_variable (path.join (location, 'DAnCE/bin'))

            script.write_newline ()

            script.write_comment ('Define the location of the libraries')
            script.append_libpath_variable (path.join (location, 'ACE/lib'))
            script.append_libpath_variable (path.join (location, 'DAnCE/lib'))

    #
    # Build the project
    #
    def build (self, prefix, type, versioned_namespace):
        import sys
        from string import Template

        ACE_ROOT = os.environ['ACE_ROOT']

        # We need to define the platform_macros.GNU script if we are not
        # running on a Windows environment.
        if not (sys.platform == 'win32'):
          logging.getLogger ().info ('defining platform_macros.GNU')

          if sys.platform == 'darwin':
            # Use the version number to select the correct platform.
            import platform
            version = platform.mac_ver ()[0]

            if version.startswith ('10.3'):
              platform_macros = 'platform_macosx_panther.GNU'
              config_file = 'config-macosx-panther.h'
            elif version.startswith ('10.4'):
              platform_macros = 'platform_macosx_tiger.GNU'
              config_file = 'config-macosx-tiger.h'
            elif version.startswith ('10.5'):
              platform_macros = 'platform_macosx_leopard.GNU'
              config_file = 'config-macosx-leopard.h'
            elif version.startswith ('10.6'):
              platform_macros = 'platform_macosx_snowleopard.GNU'
              config_file = 'config-macosx-snowleopard.h'
            elif version.startswith ('10.7'):
              platform_macros = 'platform_macosx_lion.GNU'
              config_file = 'config-macosx-lion.h'
            elif version.startswith ('10.8'):
              platform_macros = 'platform_macosx_mountainlion.GNU'
              config_file = 'config-macosx-mountainlion.h'
            elif version.startswith ('10.9'):
              platform_macros = 'platform_macosx_mavericks.GNU'
              config_file = 'config-macosx-mavericks.h'
            else:
              assert False, '*** error: unknown/unsupported version of MacOS X'

          elif sys.platform in ['linux2', 'linux']:
            platform_macros = 'platform_linux.GNU'
            config_file = 'config-linux.h'

            # Create a symbolic link to the target platform macros.
          source = path.join (ACE_ROOT, 'include/makeinclude/', platform_macros)
          target = path.join (ACE_ROOT, 'include/makeinclude/platform_macros.GNU')

          if not path.exists (target):
            cmd = ['ln', '-s', source, target]
            subprocess.check_call (cmd)

        elif sys.platform == 'win32':
          config_file = 'config-win32.h'

        # Construct the name of the target file.
        filename = path.join (ACE_ROOT, 'ace/config.h')

        if not path.exists (filename):
            # Generate the ace/config.h file
            tmpl = Template ("""// -*- C++ -*-

#ifndef _ACE_CONFIG_H_
#define _ACE_CONFIG_H_

#include "ace/${config_file}"

#endif  // !defined _ACE_CONFIG_H_
""")

            params = { 'config_file' : config_file }

            logging.getLogger ().info ('creating default ace/config.h file')
            config = open (filename, 'w')

            config.write (tmpl.substitute (params))
            config.close ()

        # First, we are going to build ACE + TAO + CIAO + DAnCE
        CIAO_ROOT = path.abspath (path.join (prefix, self.__location__, 'CIAO'))
        os.environ['CIAO_ROOT'] = CIAO_ROOT

        workspace = path.join (CIAO_ROOT, 'CIAO_TAO_DAnCE.mwc')

        features = "xerces3=1,boost=1"

        if versioned_namespace:
            features += ',versioned_namespace=1'

        from ..MpcWorkspace import MpcWorkspace
        mwc =  MpcWorkspace (workspace, type, features, True)

        mwc.generate ()
        mwc.build ()

    #
    # Build the project
    #
    def clean (self, prefix, type, versioned_namespace):
        import sys
        from string import Template

        # First, we are going to build ACE + TAO + CIAO + DAnCE
        CIAO_ROOT = path.abspath (path.join (prefix, self.__location__, 'CIAO'))
        os.environ['CIAO_ROOT'] = CIAO_ROOT

        workspace = path.join (CIAO_ROOT, 'CIAO_TAO_DAnCE.mwc')

        features = "xerces3=1,boost=1"

        if versioned_namespace:
            features += ',versioned_namespace=1'

        from ..MpcWorkspace import MpcWorkspace
        mwc =  MpcWorkspace (workspace, type, features, True)
        mwc.clean ()
