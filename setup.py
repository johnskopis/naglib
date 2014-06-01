#!/usr/bin/env python

'''Template from Requests Library: https://raw.github.com/kennethreitz/requests'''

import os
import sys

import naglib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = ('naglib',)

requires = []

with open('README.md') as f:
    readme = f.read()
with open('HISTORY.md') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='naglib',
    version=naglib.__version__,
    description='A library to generate nagios',
    long_description='None yet',
    author='John Skopis',
    author_email='jspam@skopis.com',
    url='https://github.com/johnskopis/naglib',
    packages=packages,
    package_dir={'naglib': 'naglib'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        #'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ),
)
