# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

description = """
django-pipeline compiler for browserify, requires browserify to be installed.
"""

setup(
    name='django-pipeline-browserify',
    version='0.2.0',
    description=description,
    long_description=io.open('README.rst', encoding='utf-8').read(),
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
