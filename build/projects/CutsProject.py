#!/bin/env python

################################################################################
#
# @file        CutsProject.py
#
# $Id: CutsProject.py 3707 2013-03-28 13:28:40Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

from ..Project import Project
from ..scm import Git

import os
import sys
import getopt

from os import path
import logging

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return CutsProject ()

#
# @class CutsProject
#
# Implementation of the Project class for CUTS.
#
class CutsProject (Project):
    __location__ =  path.join ('SEM', 'CUTS')

    #
    # Default constructor.
    #
    def __init__ (self):
        Project.__init__ (self, 'CUTS')

    #
    # Get the project's dependencies. The return value of this
    # function is a list of 1st level project dependencies.
    #
    def get_depends (self):
        return ['Boost', 'MPC', 'XercesC', 'DOC', 'ADBC', 'pcre', 'SQLite', 'XSC']

    #
    # Download the CUTS source files. The source files are taken from
    # trunk in the SVN repo.
    #
    def download (self, ctx):
        abspath = path.abspath (path.join (ctx.prefix, self.__location__))

        from ..scm import Git

        if ctx.affiliate:
            if ctx.use_https:
                url = 'https://github.iu.edu/SEDS/CUTS.git'
            else:
                url = 'git@github.iu.edu:SEDS/CUTS.git'

            Git.checkout (url, abspath)
        else:
            if not ctx.use_https:
                logging.getLogger ().warn ('Github only supports HTTPS checkouts.')

            url = 'https://github.com/SEDS/CUTS.git'
            Git.checkout (url, abspath)

    #
    # Update the CUTS project to its latest controlled version.
    #
    def update (self):
        CUTS_ROOT = os.environ['CUTS_ROOT']

        # Query information about the CUTS project workspace.
        info = Project.svn_info (CUTS_ROOT)
        if info is None or info == '':
            return

        # Get root information about the sandbox
        from xml.dom.minidom import parseString
        dom = parseString (info)

        root = dom.getElementsByTagName ('root')[0]

        def get_text (nodes):
            rc = []
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)

            return ''.join(rc)

        url = get_text (root.childNodes)

        # Make sure current repo is pointing to correct location.
        new_url = 'https://svn.cs.iupui.edu/repos/CUTS'

        if not url == new_url:
            import shutil
            logging.getLogger ().info ('CUTS repo has moved; updating...')

            def error_handler (func, path, exc_info):
                import stat
                if not os.access (path, os.W_OK):
                    # Is the error an access error ?
                    os.chmod (path, stat.S_IWUSR)
                    func (path)
                else:
                    raise Exception (func, path, exc_info)

            # Delete the old directoy, then do a fresh checkout
            # of CUTS from the new location.
            shutil.rmtree (CUTS_ROOT, onerror=error_handler)
            self.download ()

    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self.__location__))
        os.environ['CUTS_ROOT'] = abspath

        from ..Utilities import append_libpath_variable
        from ..Utilities import append_path_variable

        append_path_variable (path.join (abspath, 'bin'))
        append_libpath_variable (path.join (abspath, 'lib'))

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        if 'CUTS_ROOT' not in os.environ:
            logging.getLogger ().error ('CUTS_ROOT environment variable is not defined')
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

            script.begin_section ('CUTS')
            script.write_env_variable ('CUTS_ROOT', location)
            script.append_path_variable (path.join (location, 'bin'))
            script.append_libpath_variable (path.join (location, 'lib'))

    #
    # Build the project
    #
    def build (self, prefix, build_type, versioned_namespace):
        CUTS_ROOT = self.get_CUTS_ROOT ()        
        feature_file = path.join (CUTS_ROOT, 'default.features')
        
        mwc = self.get_mwc_workspace (prefix, build_type, versioned_namespace)
        mwc.generate_default_feature_file (feature_file)

        mwc.generate ()
        mwc.build ()

    #
    # Clean the project
    #
    def clean (self, prefix, build_type, versioned_namespace):
        # We are assuming the workspace is already generated
        mwc = self.get_mwc_workspace (prefix, build_type, versioned_namespace)
        mwc.clean ()
        
    #
    # Get the MWC workspace file
    #
    def get_mwc_workspace (self, prefix, build_type, versioned_namespace):
        CUTS_ROOT = self.get_CUTS_ROOT ()
        workspace = path.join (CUTS_ROOT, 'CUTS.mwc')

        if sys.platform == 'win32':
            features = 'runtime=1,boost=1,xerces3=1,ccm=1,tcpip=1,sqlite3=1,pcre=1,mfc=1,mpi=0,xsc=1'
        else:
            features = 'runtime=1,boost=1,xerces3=1,ccm=1,tcpip=1,sqlite3=1,pcre=1,mpi=0,xsc=1'

        if versioned_namespace:
            logging.getLogger ().info ('building with versioned namespace support')
            features += ',versioned_namespace=1'

        # Set features that are based on the existence of third-party
        # software that we did not install (i.e., installed by the
        # end-user).
        if 'OSPL_HOME' in os.environ:
            features += ',opensplice=1'
        else:
            features += ',opensplice=0'

        if 'NDDSHOME' in os.environ:
            features += ',ndds=1'
        else:
            features += ',ndds=0'

        if 'COSMIC_ROOT' in os.environ:
            features += ',modeling=1,cosmic=1,game=1'
        else:
            features += ',modeling=0,cosmic=0,game=0'

        if 'RTI_HOME' in os.environ:
            features += ',portico=1'
        else:
            features += ',portico=0'

        if 'TRON_ROOT' in os.environ:
            features += ',tron=1'
        else:
            features += ',tron=0'

        if 'COREDX_TOP' in os.environ:
            features += ',coredx=1'
        else:
            features += ',coredx=0'

        # Generate the workspace
        from ..MpcWorkspace import MpcWorkspace
        return MpcWorkspace (workspace, build_type, features, True)

    def get_CUTS_ROOT (self):
        return os.environ['CUTS_ROOT']
