#!/bin/env python

################################################################################
#
# @file        Project.py
#
# $Id: Project.py 3691 2012-11-06 20:43:52Z dfeiock $
#
# @author      James H. Hill
#
################################################################################

#
# @class Project
#
# Base class for all projects.
#
class Project:
    #
    # Initializing constuctor.
    #
    # @param            name            Unique name of project.
    #
    def __init__ (self, name):
        self.__name__ = name

    #
    # Get the project's name.
    #
    def name (self):
        return self.__name__


    #
    # Get the project's dependencies. The returned list is a list
    # of project objects. If this function is not overloaded, then
    # the an empty list is returned (i.e., there are not dependencies).
    #
    def get_depends (self):
        return []

    #
    # Validate the environment, ensuring that all the necessary environment
    # variables and binaries necessary for building are available.
    #
    def validate_environment (self):
      pass
        
    #
    # Download the project's source files. The download can be from an online
    # archive, or a source code repository.
    #
    # @param            prefix          Location to download
    # @param            use_trunk       Flag to download trunk version instead of stable
    # @param            use_https       Flag to download via git using https:// instead of git://
    #
    def download (self, prefix, use_trunk, use_https):
        pass

    #
    # Update the project to the latest version. What is considered
    # latest varies from project to project.
    #
    # @param            prefix          Location to update
    #
    def update (self, prefix):
        pass
    
    #
    # Update the script with details to configure the environment and
    # support the project.
    #
    # @param[in]        script          ScriptFile object
    #
    def update_script (self, prefix, script):
        pass

    #
    # Build the project.
    #
    # @param            prefix                  Location of the build
    # @param            type                    The build type
    # @param            versioned_namespace     Use versioned namespace
    #
    def build (self, prefix, type, versioned_namespace):
        pass

    #
    # Clean the project.
    #
    def clean (self, prefix, type, versioned_namespace):
        pass
        
    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        pass
