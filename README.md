[![Test & Release & Deploy](https://github.com/adamjakab/BeetsPluginBpmAnalyser/actions/workflows/test_release_deploy.yml/badge.svg)](https://github.com/adamjakab/BeetsPluginBpmAnalyser/actions/workflows/test_release_deploy.yml)
[![PyPi](https://img.shields.io/pypi/v/beets-bpmanalyser.svg)](https://pypi.org/project/beets-bpmanalyser/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/beets-bpmanalyser.svg)](https://pypi.org/project/beets-bpmanalyser/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)

# BPM Analyser (Beets Plugin)

The _beets-bpmanalyser_ plugin lets you analyse the tempo of the songs you have in your library and write the bpm information on the bpm tag of your media files.

This plugin has a more powerful big brother which does much more than just extracting bpm: [beets-xtractor plugin](https://github.com/adamjakab/BeetsPluginXtractor).

## Installation

The plugin can be installed via:

```shell script
pip install beets-bpmanalyser
```

It has three dependencies: [numpy](https://pypi.org/project/numpy/), [aubio](https://pypi.org/project/aubio/) and [pydub](https://pypi.org/project/pydub/) all of which are installed automatically when installing the plugin itself. Pydub is a wrapper library around ffmpeg or libav which are used to convert audio files to a temporary non-compressed (wav) version before running the aubio analysis on the song.

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
  threads: "AUTO"
  force: no
  quiet: no
```

By setting the `auto` option to `yes`, the plugin will be run automatically on each new item during import.

The other configuration options can also be set from the command line when running the plugin.
Here are the options explained:

_-d, --dry-run_ : Do not update the library or the media files. Only display the bpm values.

_-f, --force_ : By default only songs with no bpm value (bpm:0) are analysed. Use this option to force the analysis regardless of the current bpm value.

_-w, --write_ : Write the bpm values directly to the media files.

_-t THREADS, --threads=THREADS_: Set the number of processes to run in parallel. By default it is set to AUTO (`threads: AUTO`) and it will use half of the number of cores of your processor(s) have. You can set this to any number to specify how many concurrent threads you want to run.

_-q, --quiet_ : Do not display any output from the command.

_-v, --version_ : Displays the version number of the plugin.

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

## Issues

If something is not working as expected please use the Issue tracker.
If the documentation is not clear please use the Issue tracker.
If you have a feature request please use the Issue tracker.
In any other situation please use the Issue tracker.

## Other plugins by the same author

- [beets-goingrunning](https://github.com/adamjakab/BeetsPluginGoingRunning)
- [beets-xtractor](https://github.com/adamjakab/BeetsPluginXtractor)
- [beets-yearfixer](https://github.com/adamjakab/BeetsPluginYearFixer)
- [beets-autofix](https://github.com/adamjakab/BeetsPluginAutofix)
- [beets-describe](https://github.com/adamjakab/BeetsPluginDescribe)
- [beets-bpmanalyser](https://github.com/adamjakab/BeetsPluginBpmAnalyser)
- [beets-template](https://github.com/adamjakab/BeetsPluginTemplate)

## Acknowledgements

Many thanks to the developers and contributors of the [beets check plugin](https://github.com/geigerzaehler/beets-check). Some structural concepts and best practices were adopted to get started on this plugin.

## Final Remarks

Enjoy!
