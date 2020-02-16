# BPM Analyser (beets plugin)

*A [beets](https://github.com/beetbox/beets) plugin for insane obsessive-compulsive music geeks.*

*beets-bpmanalyser* plugin lets you analyse the tempo of the songs you have in your library and write the bpm information on the bpm tag of your media files.

## Installation
The plugin can be installed via:

```shell script
$ pip install --user beets-bpmanalyser
```

It has two dependencies: [numpy](https://pypi.org/project/numpy/) and [aubio](https://pypi.org/project/aubio/) both of which will be installed automatically when installing the plugin itself.

It is also possible to clone the git repository and install the plugin manually:

```shell script
$ git https://github.com/adamjakab/BeetsPluginBpmAnalyser
$ cd BeetsPluginBpmAnalyser
$ ./setup.py install --user
```

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

Apart from `auto` all the other configuration options can also be set from the command line when running the pulgin. Here are the options explained:

- auto []: NOT YET IMPLEMENTED! Execute the analysis during import.
- dry-run [-d, --dry-run]: Do not update the library or the media files. Only display the bpm values.
- write [-w, --write]: Write the bpm values directly to the media files.
- threads [-t THREADS, --threads=THREADS]: Set the number of processes that can run in parallel. It will default to the number of cores of your processor(s).
- force [-f, --orce]: By default only songs with no bpm value (bpm:0) are analysed. Use this option to force the analysis regardless of the current bpm value.
- quiet [-q, --quiet]: Do not display any output from the command.

## Development Notes 
Read the [plugin development](https://beets.readthedocs.io/en/stable/dev/plugins.html) section.

Take care of dependencies:
```shell script
$ pip install numpy, aubio
```

Clone the repository as described above in the installation section.

Add the path of the 'beetsplug' folder:
```yaml
pluginpath:
  - /path/to/folder/beetsplug/
  # [...]
```

If you need a custom configuration while developing you can make use of the included `dev.yml` file by using `beet -c dev.yml [CMD]`.

## Acknowledgements
Many thanks to the developers and contributors of the [beets check plugin](https://github.com/geigerzaehler/beets-check). Some structural concepts and best practices were adopted to start on this plugin. 
