#!/bin/env python

################################################################################
#
# @file        Workspace.py
#
# $Id: Workspace.py 3661 2011-12-28 22:46:33Z hillj $
#
# @author      James H. Hill
#
################################################################################

class Workspace:
  #
  # @class ProjectNotFound
  #
  # Exception thrown when a project is not found. The name of the
  # project is provided in the exception.
  #
  class ProjectNotFound (Exception):
    #
    # Initializing constructor
    #
    def __init__ (self, name):
      self.__name__ = name
      
    #
    # Get the name of the project not found.
    #
    def name (self):
      return self.__name__
    
  #
  # Default constructor
  #
  def __init__ (self, projects = []):
    self.__projects__ = projects
    
  #
  # Insert a new project into the workspace. The project is added
  # to the workspace if it does not already exist.
  #
  # @param          proj          Project object
  #
  def insert (self, proj):
    if not proj in self.__projects__:
      self.__projects__.append (proj)
      
  
  #
  # Get the specified project object
  #
  # @param          name          Name of the project
  #
  def get_project (self, name):
    for proj in self.__projects__:
      if proj.name () == name:
        return proj
      
    raise Workspace.ProjectNotFound (name)
     
  #
  # Get a list of all projects in the workspace.
  #
  def get_projects (self):
    return self.__projects__
  
  #
  # Get a project's dependencies in topological order.
  #
  # @param          name          Name of the project
  #
  def get_depends (self, name):
    # Get the project object.
    proj = self.get_project (name)
    return self.__get_depends (proj)
  
  #
  # Implementation of get_depends () where the project object
  # is provided instead of the project name.
  #
  # @param          proj          A Project object
  #
  def __get_depends (self, proj):
    current = proj.get_depends ()
    depends = []
    
    for item in current:
        p = list (filter (lambda x: x.name () == item, self.__projects__))
        
        if len (p):
          # Get the dependencies for this project object.
          children = self.__get_depends (p[0])
          
          if not children is None:
              # Append the child dependencies to the list.
              for child in children:
                  if not child in depends:
                      depends.append (child)
        
    # We can now append our dependencies to the list.
    for child in current:
      try:
        # Get the project object for this project.
        p = self.get_project (child)
        
        if not p in depends:
            depends.append (p)
            
      except Workspace.ProjectNotFound:
        pass
            
    return depends
  
  #
  # Topologically order the projects in the workspace.
  #
  def order_projects (self):
    ordering = []
    
    for proj in self.__projects__ :
        # Gather this projects dependencies. We are going to append
        # them to the ordering if there are indeed any dependencies.
        # We also need to make sure we add the name to the list once
        # and not multiple times.
        depends = self.__get_depends (proj)
        
        if not depends is None:
            for depend in depends:
                if not depend in ordering:
                    ordering.append (depend)
            
        # Now, we add ourselves to the ordering list
        if not proj in ordering:
            ordering.append (proj)
            
    return ordering
        
