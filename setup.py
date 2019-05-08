# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# This uses the template https://github.com/pypa/sampleproject/blob/master/setup.py

# To build/upload the package, do the following as described in
# https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html
# sudo python3 setup.py sdist
# sudo python3 setup.py bdist_wheel --universal
# sudo python3 setup.py sdist bdist_wheel upload

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
import sys

setup(
    name='PyNDNABS',

    version='0.0.1',

    description='Attribute-Based Signatures for Named Data Networking',

    url='https://github.com/sanjeevr93/PyNDNABS',

    maintainer='Sanjeev Kaushik Ramani',
    maintainer_email='skaus004@fiu.edu',

    license='LGPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Programming Language :: Python :: 3'
    ],

    keywords='NDN',

    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>3.3',

    install_requires=['charm-crypto', 'pyndn', 'pickledb'],

    extras_require={  # Optional
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'ndnabs=ndnabs.command_line:CommandLine',
        ],
    },
)
