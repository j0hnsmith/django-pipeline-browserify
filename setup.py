# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

description = """
django-pipeline compiler for browserify, requires browserify to be installed.
"""

setup(
    name='django-pipeline-browserify',
    version='0.1.0',
    description=description,
    long_description=description,
    author='j0hnsmith',
    url='https://github.com/j0hnsmith/django-pipeline-browserify',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
