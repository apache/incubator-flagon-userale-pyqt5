.. ..

	<!--- Licensed to the Apache Software Foundation (ASF) under one or more
	contributor license agreements.  See the NOTICE file distributed with
	this work for additional information regarding copyright ownership.
	The ASF licenses this file to You under the Apache License, Version 2.0
	(the "License"); you may not use this file except in compliance with
	the License.  You may obtain a copy of the License at

	  http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License. 
	--->

.. _installation:

Installation Guide
==================

Requirements
------------

* Python 3.5 or above
* PyQt5, version 5.3 or above
* pip3, see requirements.txt

Installing Apache UserALE.PyQt5
-------------------------------

The first step is to install Apache UserALE.PyQt5. First, checkout the latest version of Apache UserALE.PyQt5 from our Git repository.

::

	$ git clone https://git-wip-us.apache.org/repos/asf/incubator-senssoft-userale-pyqt5.git

Apache UserALE.PyQt5 is a python3 project, so it can be installed like any other python library. Several operating systems (Mac OS X, Major Versions of Linux/BSD) have Python3 pre-installed, so you should just have to run

::
	
    $ easy_install3 userale

or

::

    $ pip3 install userale

Users are strongly recommended to install Apache UserALE.PyQt5 in a virtualenv. Instructions to setup an virtual environment will be explained below.

.. note ::

	Apache UserALE.PyQt5 requires that PyQt5 and the Qt5 bindings has been installed. Instructions to install PyQt5 and Qt5 in a virtual environment will be left to the user.
	
.. note ::

	When the package is installed via ``easy_install3`` or ``pip3`` this function will be bound to the ``userale`` executable in the Python installation's ``bin`` directory (on Windows - the ``Scripts`` directory).

Installing Apache UserALE.PyQt5 in an Virtual Environment
---------------------------------------------------------

There are multiple ways to create virtual environments for a Python3 application. virtualenv is a one of those tools to create isolated Python environments. virtualenv creates a folder which contains all the necessary executables to use the packages that the UserAle project would need. 


Start by changing directory into the root of Apache UserALE.PyQt5's project directory, and then use the virtualenv command-line tool to create a new environment:

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

	$ env/bin/pip3 install -r requirements.txt

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

First, install the documentation dependencies:

::

	$ env/bin/pip3 install -r doc_requirements.txt

To build Apache UserALE.PyQt5's documentation, create a directory at the root level of ``/userale.pyqt5`` called userale.pyqt5-docs.

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