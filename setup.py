#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pipcreate',
    version='0.1.1',
    description='Automatically create a python package upload it on github, set up continuous integration so you can focus on code.',
    long_description=readme + '\n\n' + history,
    author='Matthias Bussonnier',
    author_email='bussonniermatthias@gmail.com',
    url='https://github.com/Carreau/pipcreate',
    packages=[
        'pipcreate',
    ],
    package_dir={'pipcreate':
                 'pipcreate'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pipcreate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
