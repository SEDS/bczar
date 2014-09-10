#!/bin/env python

################################################################################
#
# @file        SQLiteProject.py
#
# $Id: SQLiteProject.py 3708 2013-04-01 13:55:20Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

import os
import subprocess
import sys

from ..Project import Project
from os import path
import logging

#
# __create__
#
# Factory function for creating the project.
#
def __create__ ():
    return SQLiteProject ()
    
#
# @class SQLiteProject
#
# Implementation of the Project object for the SQLiteProject.
#
class SQLiteProject (Project):
    #
    # Default constuctor.
    #
    def __init__ (self):
        Project.__init__ (self, 'SQLite')

        if sys.platform == 'win32':
            self.__sqlite_basename__ = 'sqlite-amalgamation-3070800'
        else:
            self.__sqlite_basename__ = 'sqlite-autoconf-3070800'

    #
    # Downlaod the project's source files. The download can be from an online
    # archive, or a source code repository.
    #
    def download (self, prefix, use_trunk, use_https):
        from ..Utilities import download_url
        from ..Utilities import unpackage_archive

        abspath = path.abspath (path.join (prefix, self.__sqlite_basename__))

        if not path.exists (abspath):
            # Download the SQLite source files, which are provided in a tarball
            # that can be download from the web. We are then going to unpackage
            # the tarball so we can build it later.
            if sys.platform == 'win32':
                sqlite_archive = self.__sqlite_basename__ + '.zip'
            else:
                sqlite_archive = self.__sqlite_basename__ + '.tar.gz'

            sqlite_url = 'http://www.sqlite.org/' + sqlite_archive
            sqlite_localfile = path.join (prefix, sqlite_archive)

            download_url (sqlite_url, sqlite_localfile)

            # Unpackage the archive, and remove it from disk.
            unpackage_archive (sqlite_localfile, path.abspath (prefix))
            os.remove (sqlite_localfile)

            if sys.platform == 'win32':
                # On Windows, we need to a little extra work just to download
                # all the necessary files to build SQLite.
                sqlite_archive = 'sqlite-dll-win32-x86-3070800.zip'
                sqlite_url = 'http://www.sqlite.org/' + sqlite_archive
                sqlite_localfile = path.join (prefix, sqlite_archive)
    
                download_url (sqlite_url, sqlite_localfile)
    
                # Unpackage the archive, and remove it from disk.
                target = path.join (path.abspath (prefix), self.__sqlite_basename__)
                unpackage_archive (sqlite_localfile, target)
                os.remove (sqlite_localfile)
    
                # Now, we need to run LIB on the dll to create the input
                # library for SQLite.
                cmd = ['lib', '/DEF:sqlite3.def', '/MACHINE:X86']
                subprocess.check_call (cmd, cwd = abspath)
    
                include = path.join (abspath, 'include')
                libpath = path.join (abspath, 'lib')
    
                files = {'include' : ['sqlite3.h', 'sqlite3ext.h'],
                         'lib'     : ['sqlite3.dll', 'sqlite3.lib', 'sqlite3.exp'] }
    
                unlink = ['shell.c', 'sqlite3.c', 'sqlite3.def']
    
                for relpath, filelist in files.items ():
                    import shutil
    
                    # Make the target directory for the relative path.
                    target = path.join (abspath, relpath)
                    os.mkdir (target)
    
                    # Move each file into the target directory.
                    for file in filelist:
                        shutil.move (path.join (abspath, file), target)
    
                # Finally, remove all unnecessary files.
                for file in unlink:
                    os.remove (path.join (abspath, file))
 
    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        abspath = path.abspath (path.join (prefix, self.__sqlite_basename__))
        os.environ['SQLITE_ROOT'] = abspath

        append_path_variable (path.join (abspath, 'bin'))
        append_libpath_variable (path.join (abspath, 'lib'))

    #
    # Validate environment for the project
    #
    def validate_environment (self):
        if 'SQLITE_ROOT' not in os.environ:
            logging.getLogger ().error ('SQLITE_ROOT environment variable is not defined')
            return False

        return True

    #
    # Update the script with details to configure the environment and
    # support the project.
    #
    # @param[in]            script          ScriptFile object
    #
    def update_script (self, prefix, script):
        abspath = path.abspath (path.join (prefix, self.__sqlite_basename__))

        if path.exists (abspath):
            script_path = script.get_this_variable ()
            location = os.path.join (script_path, self.__sqlite_basename__)

            script.begin_section ('SQLite')
            script.write_env_variable ('SQLITE_ROOT', location)
            script.append_path_variable (path.join (location, 'bin'))
            script.append_libpath_variable (path.join (location, 'lib'))

    #
    # Build the project
    #
    def build (self, prefix, type, versioned_namespace):
        SQLITE_ROOT = os.environ['SQLITE_ROOT']

        if sys.platform == 'win32':
          pass
        else:
          # Configure SQLite build environment
          cmd = ['./configure', '--prefix=' +  SQLITE_ROOT]
          __ap__ = subprocess.Popen (cmd, cwd = SQLITE_ROOT)
          __ap__.wait ()

          # We can now build SQLite.
          cmd = ['make', 'install']
          __ap__ = subprocess.Popen (cmd, cwd = SQLITE_ROOT)
          __ap__.wait ()

    #
    # Build the project
    #
    def clean (self, prefix, type, versioned_namespace):
        SQLITE_ROOT = os.environ['SQLITE_ROOT']

        if sys.platform == 'win32':
          pass
        else:
          # We can now build SQLite.
          cmd = ['make', 'clean']
          __ap__ = subprocess.Popen (cmd, cwd = SQLITE_ROOT)
          __ap__.wait ()
