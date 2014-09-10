#!/bin/env python

################################################################################
#
# @file        Git.py
#
# $Id: Git.py 3708 2013-04-01 13:55:20Z dfeiock $
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
# @param[in]        branch      Branch or tag to checkout
#
def checkout (url, location, username=None, password=None, branch=None):
  from os import path
  from urllib.parse import urlparse, urlunparse

  if path.exists (os.path.join (location, '.git')):
    logging.getLogger ().info ('{0} is not an empty directory; skipping download'.format (location))
    return

  if not 'GIT_SSL_NO_VERIFY' in os.environ:
    os.environ['GIT_SSL_NO_VERIFY'] = 'true'

  parsed_url = list(urlparse (url))
  prepend_string = ""

  if username is not None:
    prepend_string = username

  if password is not None:
    prepend_string = "%s:%s" (prepend_string, password)

  if len(prepend_string) is not 0:
    parsed_url[1] = "%s@%s" (prepend_string, parsed_url[1])
    url = urlunparse (parsed_url)

  cmd = ["git", "clone", "--quiet"]
  if branch:
    cmd.extend (['--branch', branch])
  cmd.extend ([url, location])
  subprocess.check_call (cmd)

  # Checkout submodules if there are any
  cmd = ["git", "submodule", "update", "--init"]
  subprocess.check_call (cmd, cwd = location)
        
#
# Get information about the Git location.
#
def info (location):
  cmd = ["git", "remote", "-v", location]
  return subprocess.check_output (cmd)

