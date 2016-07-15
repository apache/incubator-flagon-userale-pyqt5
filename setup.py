# -*- coding: utf-8 -*-
#
# Copyright 2016 The Charles Stark Draper Laboratory, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from __future__ import absolute_import
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io, os, sys

if sys.version_info[:2] < (3, 5):
    m = "Python 3.5 or later is required for UserAle (%d.%d detected)."
    raise ImportError (m % sys.version_info[:2])

if sys.argv[-1] == 'setup.py':
    print ("To install, run 'python3 setup.py install'")
    print ()
    
def read (*filenames, **kwargs):
    encoding = kwargs.get ('encoding', 'utf-8')
    sep = kwargs.get ('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open (filename, encoding=encoding) as f:
            buf.append (f.read ())
    return sep.join (buf)


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest (TestCommand):
    def finalize_options (self):
        TestCommand.finalize_options (self)
        self.test_args = []
        self.test_suite = True

    def run_tests (self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit (pytest.main (self.test_args))

# Get the version string 
g = {}
with open (os.path.join ('userale', 'version.py'), 'rt') as f:
    exec (f.read (), g)
    version = g['__version__']

setup (
    name = 'UserAle',
    version = version,
    url = 'https://github.com/draperlaboratory/userale.pyqt5',
    license = 'Apache Software License',
    author = 'Michelle Beard',
    author_email = 'mbeard@draper.com',
    description = 'UserAle provides an easy way to generate highly detailed log streams from a PyQt5 application.',
    long_description = __doc__,
    classifiers = [
      'Development Status :: 4 - Beta',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3.5',
      'Natural Language :: English',
      'Environment :: Desktop Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent', 
      'Private :: Do Not Upload"'
    ],
    keywords = 'logs users interactions', # Separate with spaces
    packages = find_packages (exclude=['examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
    install_requires = ['pyqt5==5.6', 
                        'requests>=2.0.0'
                        ],
    entry_points = {
        'console_scripts': [
            'mouse = userale.tests.testapp:test_app',
            'drag = userale.tests.testdragndrop:test_drag',
            'drag2 = userale.tests.testdragndrop2:test_drag2'
        ]
    }
)
