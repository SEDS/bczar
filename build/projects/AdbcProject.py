#!/bin/env python

################################################################################
#
# @file        AdbcProject.py
#
# $Id: AdbcProject.py 3706 2013-03-18 16:57:53Z dfeiock $
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
def __create__():
  return AdbcProject()


#
# @class AdbcProject
#
# Implemenation of the Project object for building the ADBC
# source code.
#
class AdbcProject(Project):
  __location__ = 'Middleware/ADBC'

  #
  # Default constructor.
  #
  def __init__(self):
    Project.__init__(self, 'ADBC')

  #
  # Get the project's dependencies. The return value of this
  # function is a list of 1st level project dependencies.
  #
  def get_depends(self):
    return ['SQLite', 'MPC', 'DOC']

  #
  # Download the project's source files. The download can be from an online
  # archive, or a source code repository.
  #
  def download(self, ctx):
    if ctx.use_https:
      url = 'https://github.com/DOCGroup/ADBC.git'
    else:
      url = 'git@github.com:DOCGroup/ADBC.git'

    abspath = path.abspath(path.join(ctx.prefix, self.__location__))
    Git.checkout(url=url, location=abspath)

  #
  # Set the project's environment variables.
  #
  def set_env_variables(self, prefix):
    abspath = path.abspath(path.join(prefix, self.__location__))

    from ..Utilities import append_libpath_variable
    from ..Utilities import append_path_variable

    os.environ['ADBC_ROOT'] = path.join(abspath, 'ADBC')
    append_libpath_variable(path.join(abspath, 'ADBC', 'lib'))

  #
  # Validate environment for the project
  #
  def validate_environment(self):
    if 'ADBC_ROOT' not in os.environ:
      logging.getLogger().error('ADBC_ROOT environment variable is not defined')
      return False

    return True

  #
  # Update the script with details to configure the environment and
  # support the project.
  #
  # @param[in]            script          ScriptFile object
  #
  def update_script(self, prefix, script):
    abspath = path.abspath(path.join(prefix, self.__location__))

    if path.exists(abspath):
      script_path = script.get_this_variable()

      script.begin_section('ADBC')
      script.write_env_variable('ADBC_ROOT', path.join(script_path, self.__location__))

      script.write_newline()

      script.write_comment('Define the location of the libraries')
      script.append_libpath_variable(path.join(script_path, self.__location__, 'lib'))

  #
  # Build the project
  #
  def build(self, ctx):
    mwc = self.get_mwc_workspace(ctx)

    ADBC_ROOT = self.get_ADBC_ROOT()
    feature_file = path.join(ADBC_ROOT, 'default.features')
    mwc.generate_default_feature_file(feature_file)

    mwc.generate()
    mwc.build()

  #
  # Clean the project
  #
  def clean(self, ctx):
    # We are assuming the workspace is already generated
    mwc = self.get_mwc_workspace(ctx)
    mwc.clean()

  #
  # Get the MWC workspace file
  #
  def get_mwc_workspace(self, ctx):
    # Now, we are goig to build ADBC
    ADBC_ROOT = self.get_ADBC_ROOT()
    workspace = path.join(ADBC_ROOT, 'ADBC.mwc')

    features = 'sqlite3=1'

    if ctx.versioned_namespace:
      features += ',versioned_namespace=1'

    from ..MpcWorkspace import MpcContext, MpcWorkspace
    mpc_ctx = MpcContext(workspace, ctx.build_type, ctx.config, ctx.threads, features, True)
    return MpcWorkspace(mpc_ctx)

  def get_ADBC_ROOT(self):
    return os.environ['ADBC_ROOT']
