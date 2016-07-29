.. _installation:

Installation Guide
==================

Requirements
------------

* Python 3.5 or above
* PyQt5, version 5.3 or above
* pip3, see requirements.txt

Installing UserAle
------------------

The first step is to install UserAle. First, checkout the latest version of UserAle from our Github repository.

::

	$ git clone https://github.com/draperlaboratory/userale.pyqt5.git

UserAle is a python3 project, so it can be installed like any other python library. Several operating systems (Mac OS X, Major Versions of Linux/BSD) have Python3 pre-installed, so you should just have to run

::
	
    $ easy_install3 userale

or

::

    $ pip3 install userale

Users are strongly recommended to install UserAle in a virtualenv. Instructions to setup an virtual environment will be explained below.

.. note ::

	UserAle.pyqt5 requires that PyQt5 and the Qt5 bindings has been installed. Instructions to install PyQt5 and Qt5 in a virtual environment will be left to the user.
	
.. note ::

	When the package is installed via ``easy_install3`` or ``pip3`` this function will be bound to the ``userale`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

Installing UserAle in an Virtual Environment
--------------------------------------------

There are multiple ways to create virtual environments for a Python3 application. virtualenv is a one of those tools to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that the UserAle project would need. 


Start by changing directory into the root of UserAle's project directory, and then use the virtualenv command-line tool to create a new environment:

::
	
	$ virtualenv --python=/usr/bin/python3 env


Optionally, Python3 has built in support for virtual environments. 

::

	$ mkdir env 
	$ python3 -m venv env

Activate environment:

::

	$ source env/bin/activate

Install UserAle requirements:

::

	$ env/bin/pip3 -r requirements.txt

To build the source code and run all unit tests.

::

    $ env/bin/python3 setup.py develop test

Deactivate environment

:: 	

	$ deactivate

Installing Documentation 
------------------------

To save yourself the trouble, all up to date documentation is available at https://draperlaboratory.github.io/userale.pyqt5/.

However, if you want to manully build the documentation, the instructions are below.

To build UserAle's documentation, create a directory at the root level of ``/userale.pyqt5`` called userale.pyqt5-docs.

::

	$ mkdir userale.pyqt5-docs & cd userale.pyqt5-docs

Execute build command:

::

	# Inside top-level docs/ directory.
 	$ make html

This should build the documentation in your shell, and output HTML. At then end, it should say something about documents being ready in ``userale.pyqt5-docs/html``. 

You can now open them in your browser by typing

::

	$ open userale.pyqt5-docs/html/index.html