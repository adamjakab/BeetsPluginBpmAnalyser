[![Build Status](https://travis-ci.org/adamjakab/BeetsPluginBpmAnalyser.svg?branch=master)](https://travis-ci.org/adamjakab/BeetsPluginBpmAnalyser)
[![Coverage Status](https://coveralls.io/repos/github/adamjakab/BeetsPluginBpmAnalyser/badge.svg?branch=master)](https://coveralls.io/github/adamjakab/BeetsPluginBpmAnalyser?branch=master)
[![PyPi](https://img.shields.io/pypi/v/beets-bpmanalyser.svg)](https://pypi.org/project/beets-bpmanalyser/)


# BPM Analyser (beets plugin)

*A [beets](https://github.com/beetbox/beets) plugin for insane obsessive-compulsive music geeks.*

The *beets-bpmanalyser* plugin lets you analyse the tempo of the songs you have in your library and write the bpm information on the bpm tag of your media files.


## Installation
The plugin can be installed via:

```shell script
$ pip install beets-bpmanalyser
```

It has two dependencies: [numpy](https://pypi.org/project/numpy/) and [aubio](https://pypi.org/project/aubio/) both of which will be installed automatically when installing the plugin itself.


## Usage
Activate the plugin in your configuration file:

```yaml
plugins:
  - bpmanalyser
  # [...]
```

Check if plugin is loaded with `beet version`. It should list 'bpmanalyser' amongst the loaded plugins.

Your default configuration is:
```yaml
bpmanalyser:
  auto: no
  dry-run: no
  write: yes
  threads: 2
  force: no
  quiet: no
```

Heads up! THe `auto` option is NOT YET IMPLEMENTED! It will be used to execute the analysis during import.


The other configuration options can also be set from the command line when running the plugin. 
Here are the options explained:

*-d, --dry-run*     : Do not update the library or the media files. Only display the bpm values.

*-f, --force*       : By default only songs with no bpm value (bpm:0) are analysed. Use this option to force the analysis regardless of the current bpm value.

*-w, --write*       : Write the bpm values directly to the media files.

*-t THREADS, --threads=THREADS*: Set the number of processes that can run in parallel. It will default to the number of cores of your processor(s).

*-q, --quiet*       : Do not display any output from the command.

*-v, --version*     : Displays the version number of the plugin.


    
### Examples:

Calculate but show only (do not store) tempo information on all AC/DC songs:

    $ beet bpmanalyser --dry-run artist:AC/DC
    
Update tempo information on all songs where it is missing:

    $ beet bpmanalyser bpm:0
    
Force the update of tempo information on all songs where it has already been set:

    $ beet bpmanalyser -f ^bpm:0


## Accuracy
BPM values from acousticbrainz:
```shell script
$ beet -c dev.yml acousticbrainz artist:AC/DC
acousticbrainz: getting data for: [format:MP3][bpm:121.106361389] ::: /_TmpMusic_/A/AC_DC/High Voltage/01. Baby, Please Don't Go.mp3
acousticbrainz: getting data for: [format:MP3][bpm:117.203399658] ::: /_TmpMusic_/A/AC_DC/High Voltage/02. She's Got Balls.mp3
acousticbrainz: getting data for: [format:MP3][bpm:106.826393127] ::: /_TmpMusic_/A/AC_DC/High Voltage/03. Little Lover.mp3
acousticbrainz: getting data for: [format:MP3][bpm:119.486862183] ::: /_TmpMusic_/A/AC_DC/High Voltage/04. Stick Around.mp3
acousticbrainz: getting data for: [format:MP3][bpm:133.189102173] ::: /_TmpMusic_/A/AC_DC/High Voltage/05. Soul Stripper.mp3
acousticbrainz: getting data for: [format:MP3][bpm:128.054992676] ::: /_TmpMusic_/A/AC_DC/High Voltage/06. You Ain't Got a Hold on Me.mp3
acousticbrainz: getting data for: [format:MP3][bpm:123.012046814] ::: /_TmpMusic_/A/AC_DC/High Voltage/07. Love Song.mp3
acousticbrainz: getting data for: [format:MP3][bpm:136.914703369] ::: /_TmpMusic_/A/AC_DC/High Voltage/08. Show Business.mp3
```

BPM values calculated by aubio:
```shell script
$ beet -c dev.yml bpmanalyser artist:AC/DC -df
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/01. Baby, Please Don't Go.mp3] bpm: 122
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/02. She's Got Balls.mp3] bpm: 117
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/03. Little Lover.mp3] bpm: 106
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/04. Stick Around.mp3] bpm: 120
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/05. Soul Stripper.mp3] bpm: 132
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/06. You Ain't Got a Hold on Me.mp3] bpm: 128
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/07. Love Song.mp3] bpm: 125
bpmanalyser: Song[/_TmpMusic_/A/AC_DC/High Voltage/08. Show Business.mp3] bpm: 139
```
 

## Development Notes 
Read the [development](./DEVELOPMENT.md) docs.


## Acknowledgements
Many thanks to the developers and contributors of the [beets check plugin](https://github.com/geigerzaehler/beets-check). Some structural concepts and best practices were adopted to start on this plugin. 
