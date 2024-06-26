#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 11:52 PM
#  License: See LICENSE.txt

import pathlib
from setuptools import setup
from distutils.util import convert_path

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

main_ns = {}
ver_path = convert_path('beetsplug/bpmanalyser/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# Setup
setup(
    name='beets-bpmanalyser',
    version=main_ns['__version__'],
    description='A beets plugin for analysing tempo of songs and storing it in the bpm tag.',
    author='Adam Jakab',
    author_email='adam@jakab.pro',
    url='https://github.com/adamjakab/BeetsPluginBpmAnalyser',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    platforms='ALL',
    test_suite='test',
    
    include_package_data=True,
    packages=['beetsplug.bpmanalyser'],
    
    python_requires='>=3.8',

    install_requires=[
        'beets>=1.4.9',
        'aubio',
        'numpy',
        'pydub'
    ],

    tests_require=[
        'pytest', 'nose', 'coverage',
        'mock', 'six'
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
