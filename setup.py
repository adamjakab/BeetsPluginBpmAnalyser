import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setup
setup(
    name='beets-bpmanalyser',
    version='1.1.0',
    description='A beets plugin for analysing tempo of songs and storing it in the bpm tag.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Adam Jakab',
    author_email='adam@jakab.pro',
    url='https://github.com/adamjakab/BeetsPluginBpmAnalyser',
    license='MIT',
    platforms='ALL',
    include_package_data=True,

    test_suite='test',

    packages=['beetsplug'],

    install_requires=[
        'beets>=1.4.3',
        'numpy',
        'aubio'
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
