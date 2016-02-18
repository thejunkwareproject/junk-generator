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


# parse requirements for python 2
if sys.version_info[0] == 2:
    with open('requirements-python2.txt') as f:
        required += [dep for dep in f.read().splitlines() if dep != "-r requirements.txt"]
setup(
      name = "junkware",
      packages = find_packages(exclude=['tests']) ,
      version = version,
      description = "Patent Junk Generator",
      long_description = long_description,
      author = "Clément Renaud",
      author_email = "clement.renaud@gmail.com",
      url = "http://junkware.io",
      download_url = "http://github.com/thejunkwareproject/junkware",
      include_package_data=True,
      keywords = ["network", "visualization", "NLP"],
      entry_points={
        'console_scripts': [
            'junkware = junkware:junkware'
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
