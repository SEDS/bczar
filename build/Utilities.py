#!/usr/bin/env python

###############################################################################
#
# @file        Utilities.py
#
# $Id: Utilities.py 3701 2012-12-20 18:03:07Z dfeiock $
#
# @author      James H. Hill
#
###############################################################################

import os
import sys
import logging

#
# Test if the script is running on a Windows platform.
#
def is_windows_platform ():
    return sys.platform.startswith ('win32')

#
# Utility function to append a value to the PATH variable
#
def append_path_variable (value):
  logging.getLogger ().info ("appending {0} to PATH".format (value))

  if is_windows_platform ():
    if 'PATH' in os.environ:
      os.environ['PATH'] = '%s;%s' % (os.environ['PATH'], value)
    else:
      os.environ['PATH'] = value
  else:
    if 'PATH' in os.environ:
      os.environ['PATH'] = '%s:%s' % (os.environ['PATH'], value)
    else:
      os.environ['PATH'] = value

#
# Utility function to append a value to the libary variable. Depending
# on the platform, this can be PATH, LD_LIBRARY_PATH, or DYLD_LIBRARY_PATH.
#
def append_libpath_variable (value):
  logging.getLogger ().info ("appending {0} to library path".format (value))

  if is_windows_platform ():
    if 'PATH' in os.environ:
      os.environ['PATH'] = '%s;%s' % (os.environ['PATH'], value)
    else:
      os.environ['PATH'] = value
  elif sys.platform == 'darwin':
    if 'DYLD_LIBRARY_PATH' in os.environ:
      os.environ['DYLD_LIBRARY_PATH'] = '%s:%s' % (os.environ['DYLD_LIBRARY_PATH'], value)
    else:
      os.environ['DYLD_LIBRARY_PATH'] = value
  elif sys.platform in ['linux2', 'linux']:
    if 'LD_LIBRARY_PATH' in os.environ:
      os.environ['LD_LIBRARY_PATH'] = '%s:%s' % (os.environ['LD_LIBRARY_PATH'], value)
    else:
      os.environ['LD_LIBRARY_PATH'] = value

#
# Download a file from the internet.
#
# @param[in]            url             URL of file to download
# @param[in]            target          Local filename
#
def download_url (url, target):
  import urllib.request
  
  logging.getLogger ().info ("downloading {0}".format (url))
  webfile = urllib.request.urlopen (url)
  
  logging.getLogger ().info ("saving file to {0}".format (target))
  local_file = open (target, 'wb')
  local_file.write (webfile.read ())
  
  local_file.close ()
  webfile.close ()

#
# Utility method for unpackaging an archive. This method can be used
# with .zip, .tar.gz., and .tar files. It will automatically detect
# the file type, and perform the appropriate actions in the tarball
# to unpackage it.
#
# @param[in]            archive             Archive to unpackage
# @param[in]            path                Location to unpackage content
#
def unpackage_archive (archive, path):
  logging.getLogger ().info ("extracting contents of {0} to {1}".format (archive, path))

  if archive.endswith ('.tar.gz') or archive.endswith ('.tar'):
    import tarfile

    tar = tarfile.open (archive)
    tar.extractall (path = path)
    tar.close()

  elif archive.endswith ('.zip'):
    import zipfile

    zip = zipfile.ZipFile (archive)
    zip.extractall (path = path)
    zip.close ()

#
# Utility function that return the Visual Studio build command. This
# will either be the command for the full-blown version of Visual
# Studio, or the express version. We, however, give precedence to the
# full version of Visual Studio
#
def get_vc_executable ():
  files = ['devenv.com', 'VCExpress.exe']

  for PATH in os.environ['PATH'].split (';'):
    for file in files:
      if os.path.exists (os.path.join (PATH, file)):
        if file == 'VCExpress.exe':
          logging.getLogger ().warning ('express edition does not show compile progress...')
          logging.getLogger ().warning ('please be patient...')

        return file

#
# Auto-detect the build type for the script. This function checks the
# OS platform, and set environment variables to determine the correct
# build type. If the build type cannot be auto-detected, then None
# is returned.
#
def autodetect_build_type ():
  sys.stdout.write ('*** info: auto-detecting build type... ')
  platform = sys.platform

  if platform in ['darwin', 'linux2', 'linux']:
    type = 'gnuace'
  else:
    import re
    import subprocess
    
    # Execute the cl.exe command. This will print the version informatino
    # to the screen, along with a LOT of other garbage!
    p = subprocess.Popen (['cl'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    output = p.communicate ()[1]
    
    # The first line of the output contains the version number, but we
    # must locate it in the line!
    pattern = '(?P<version_major>\d+)\.(?P<version_minor>\d+)\.\d+(\.\d+)?'
    match = re.search (pattern, repr (output))

    if match is None:
      assert False, '*** error: failed to locate cl.exe version'

    # Right now, the 8th word on the line is the version number.
    version_major = match.group ('version_major')
    version_minor = match.group ('version_minor')


    if version_major == '18':
      type = 'vc12'
    elif version_major == '17':
      type = 'vc11'
    elif version_major == '16':
      type = 'vc10'
    elif version_major == '15':
      type = 'vc9'
    elif version_major == '14':
      type = 'vc8'
    elif version_major == '13' and version_minor == '10':
      type = 'vc71'
    elif version_major == '13':
      type = 'vc7'
    else:
      assert False, '*** error: unknown cl.exe version (%s.%s)' % (version_major, version_minor)

  sys.stdout.write ('%s\n' % type)
  return type
