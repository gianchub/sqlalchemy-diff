#!/usr/bin/env python
from codecs import open
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as stream:
    readme = stream.read()


setup(
    name='sqlalchemy-diff',
    version='0.1.5',
    description='Compare two database schemas using sqlalchemy.',
    long_description=readme,
    author='student.com',
    author_email='wearehiring@student.com',
    url='https://github.com/gianchub/sqlalchemy-diff',
    packages=find_packages(exclude=['docs', 'test', 'test.*']),
    install_requires=[
        "sqlalchemy-utils>=0.32.4",
    ],
    extras_require={
        'dev': [
            "mysql-connector-python-rf==2.2.2",
            "pytest==6.2.2",
            "pylint==2.7.2",
            "flake8==3.8.4",
            "coverage==5.5",
        ],
        'docs': [
            "sphinx==1.4.1",
        ],
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
