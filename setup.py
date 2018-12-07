#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md') as readme:
	long_description = readme.read()

#with open('requirements.txt') as requirements:
#	install_requires = requirements.read()


setup(
    name='dtudiscrete',
    version='1.0',
    description='Helper scripts for DTU discrete math course',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='John Doe',
    author_email='more.spam.plz@mail.com',
    url='https://www.github.com/volesen/dtudiscrete',
    #packages=find_packages(exclude=('tests',)),
    py_modules=['dtudiscrete'],
    entry_points={
         'console_scripts': ['dtudiscrete=dtudiscrete.cli:cli'],
    },
    install_requires=['click', 'tabulate'],
    test_requires=['pytest'],
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)