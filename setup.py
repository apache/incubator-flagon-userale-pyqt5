# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import os
import sys


if sys.version_info[:2] < (3, 5):
    m = "Python 3.5 or later is required for UserAle (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])

if sys.argv[-1] == 'setup.py':
    print ("To install, run 'python3 setup.py install'")
    print ()


# Get the version string
def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'userale/version.py')) as f:
        version = {}
        exec(f.read(), version)
        return version['__version__']
    raise RuntimeError('No version info found.')


setup(
    name='Apache UserALE.PyQt5',
    version=get_version(),
    url='https://github.com/apache/incubator-senssoft-userale-pyqt5',
    license='Apache Software License 2.0',
    author='Michelle Beard',
    author_email='msbeard@apache.org',
    description='Apache UserALE.PyQt5 provides an easy way to generate highly\
     detailed log streams from a PyQt5 application.',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    keywords='logs users interactions',
    packages=find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest>=3.0.0', 'pytest-pylint', 'coverage'],
    install_requires=['pyqt5==5.7', 'requests>=2.0.0'],
    entry_points={
        'console_scripts': [
            'mouse = userale.examples.testapp:test_app',
            'drag = userale.examples.testdragndrop:test_drag',
            'drag2 = userale.examples.testdragndrop2:test_drag2',
            'window = userale.examples.testclose:test_close',
            'controller = userale.examples.testwindowflags:test_controller'
        ]
    }
)
