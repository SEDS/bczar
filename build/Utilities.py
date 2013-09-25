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

#
# Test if the script is running on a Windows platform.
#
def is_windows_platform ():
    return sys.platform.startswith ('win32')

#
# Utility function to append a value to the PATH variable
#
def append_path_variable (value):
  print ("*** appending %s to PATH" % value)

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
  print ("*** appending %s to library path" % value)

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
  
  print ('*** info: downloading ' + url)
  webfile = urllib.request.urlopen (url)
  
  print ('*** info: saving file to ' + target)
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
  print ('*** info: extracting contents of ' + archive + ' to ' + path)

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
          print ('*** warning: express edition does not show compile progress...')
          print ('*** warning: please be patient...')

        return file
