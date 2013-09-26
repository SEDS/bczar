Build Czar (bczar)
==================

This is a custom framework for building different middleware frameworks and
its dependencies. This include downloading source files from their respective
locations.

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
