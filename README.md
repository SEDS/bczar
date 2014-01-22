Build Czar (bczar)
==================

This is a custom framework for building different middleware frameworks and
its dependencies. 

Quick Start
-----------

We assume that you have [Python 3.x](http://python.org/download/) installed
as Python 2.x will not work. The following commands will download all source files
and build them:

    %> python3 bczar.py --prefix=[sandbox] download
    %> python3 bczar.py --prefix=[sandbox] build

Use the --help option to see the different command-line options:

    %> python3 bczar.py --help

To see the help for a given command:

    %> python3 bczar.py --help [command]

Additional Requirements
------------------------

Depending on what middleware you are building with the scripts, you may
need the following applications installed:

* Subversion
* Git
* Perl (ActivePERL on Windows)

Each of the applications needs to be able to work from the command-line.
