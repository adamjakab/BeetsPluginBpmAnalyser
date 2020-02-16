from setuptools import setup

setup(
    name='beets-bpmanalyser',
    version='1.0.0',
    description='A beets plugin analysing tempo on songs and storing it in the bpm tag.',
    long_description=open('README.md').read(),
    author='Adam Jakab',
    author_email='adam@jakab.pro',
    url='https://github.com/adamjakab/BeetsPluginBpmAnalyser',
    license='MIT',
    platforms='ALL',

    test_suite='test',

    packages=['beetsplug'],

    install_requires=[
        'beets>=1.4.9',
        'numpy',
        'aubio'
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
    ],
)
