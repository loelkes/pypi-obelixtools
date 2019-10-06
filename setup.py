#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='obelixtools',
    version='1.1.1',
    author='Christian Lölkes',
    author_email='christian.loelkes@gmail.com',
    description='Useful tools I need in many projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/loelkes/pypi-obelixtools',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
    install_requires=[
          'requests',
          'requests[security]',
          'sseclient'
      ],
)
