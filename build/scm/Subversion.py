#!/bin/env python

################################################################################
#
# @file        Subversion.py
#
# $Id: Subversion.py 3708 2013-04-01 13:55:20Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

import os
import subprocess
import logging

#
# Utility function for executing an SVN checkout
#
# @param[in]        url         Location of the repo
# @param[in]        location    Sandbox of the checkout
# @param[in]        username    Username for checkout, if applicable
# @param[in]        password    Password for checkout, if applicable
#
def checkout (url, location, username=None, password=None):
  from os import path
  
  if path.exists (os.path.join (location, '.svn')):
    logging.getLogger ().info ('{0} is not an empty directory; skipping download'.format (location))
    return

  cmd = ["svn", "--non-interactive", "--trust-server-cert", "co", url, location]

  if username is not None:
    cmd.append ("--username")
    cmd.append (username)

  if password is not None:
    cmd.append ("--password")
    cmd.append (password)

  subprocess.check_call (cmd)
        
#
# Get information about the SVN location.
#
def info (location):
  cmd = ["svn", "info", "--xml", location]
  return subprocess.check_output (cmd)

#
# Identify the latest version from the provided url
#
# @param[in]        url               Location of the repo, searches subdirectories
# @param[in]        prefix            Prefix of directories to consider
# @param[in]        version_format    Regex string for valid version numbers
# @param[in]        username          Username for svn, if applicable
# @param[in]        password          Password for svn, if applicable
def latest_version (url, prefix, version_format, username=None, password=None):
  from distutils.version import LooseVersion
  from urllib.parse import urljoin
  import re

  cmd = ["svn", "--non-interactive", "--trust-server-cert", "ls", url]

  if username is not None:
    cmd.append ("--username")
    cmd.append (username)

  if password is not None:
    cmd.append ("--password")
    cmd.append (password)

  p = subprocess.Popen (cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  output = p.communicate ()[0]

  version = re.compile (version_format);
  results = []

  for line in output.decode ().splitlines():
    if not line.startswith (prefix):
      continue

    if not version.match (line.split (prefix)[1][:-1]):
      continue

    results.append (line)

  if not url.endswith('/'):
    url += '/'

  results.sort (key=LooseVersion)
  logging.getLogger ().info ('{0} is the latest version'.format (results[-1]))
  return urljoin (url, results[-1])
