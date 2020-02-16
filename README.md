# Going Running (beets plugin)

### Installation
Take care of dependencies:

```shell script
$ pip install numpy, aubio
```

Clone the repository (working on pip...).


### Development Notes 
Read the [plugin development](https://beets.readthedocs.io/en/stable/dev/plugins.html) section.

Add the path of the 'beetsplug' folder to your configuration and activate the plugin:

```yaml
pluginpath:
    - /path/to/folder/beetsplug/
    - ...

plugins:
    - bpmanalyser
    - ...
```

Check if plugin is loaded with `beet version`. It should list 'bpmanalyser' amongst the loaded plugins.


### Acknowledgements
Many thanks to the developers and contributors of the [beets check plugin](https://github.com/geigerzaehler/beets-check). Some structural concepts and best practices were adopted to start on this plugin. 
