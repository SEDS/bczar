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
    # @param            context         Context object containing various parameters for
    #                                   managing the download
    #
    def download (self, context):
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
    # @param            context         Context object containing various parameters for
    #                                   managing the build
    #
    def build (self, context):
        pass

    #
    # Clean the project.
    #
    def clean (self, context):
        pass
        
    #
    # Set the project's environment variables.
    #
    def set_env_variables (self, prefix):
        pass
