# junkware setup.py

"""Setup script for Junwkare."""

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# Leave the following line to match the regexp [0-9]*\.[0-9]*\.[0-9]*
version = "0.0.1" # [major].[minor].[release]

# parse README
with open('README.md') as readme_file:
    long_description = readme_file.read()

# parse requirements
with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if 'git+https' not in x] # TODO - how to fix this?

setup(
      name = "junkware",
      packages = find_packages(exclude=['tests']) ,
      version = version,
      description = "Patent Junk Generator",
      long_description = long_description,
      author = "Clement Renaud",
      author_email = "clement.renaud@gmail.com",
      url = "http://junkware.io",
      download_url = "http://github.com/thejunkwareproject/junkware",
      include_package_data=True,
      keywords = ["network", "visualization", "NLP"],
      entry_points={
        'console_scripts': [
            'junkware = junkware.junkware:main'
        ],
    },
    license='GPL',
    classifiers = [
      "Programming Language :: Python",
      "Environment :: Other Environment",
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
      "Operating System :: OS Independent",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Topic :: Text Processing :: Linguistic",
    ],
    install_requires=required
    )
