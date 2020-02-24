# Development Notes 

This document for now is mostly for myself. Sorry for the mess ;)

## General
Read the [plugin development](https://beets.readthedocs.io/en/stable/dev/plugins.html) section.

Take care of dependencies:
```shell script
$ pip install numpy, aubio
```

Clone the repository and set up the plugin manually:

```shell script
$ git https://github.com/adamjakab/BeetsPluginBpmAnalyser
$ cd BeetsPluginBpmAnalyser
$ ./setup.py install
```

Add the path of the 'beetsplug' folder and add the name of the plugin to activate it:
```yaml
pluginpath:
  - /path/to/BeetsPluginBpmAnalyser/beetsplug/
  # [...]
plugins:
  - bpmanalyser
  # [...]
```

If you need a custom configuration while developing you can make use of the included `dev.yml` file by using `beet -c dev.yml [CMD]`.


## Deployment of a new version

I guess this is mostly for me:

```shell script
$ bumpversion --current-version 1.0.0 minor setup.py
$ rm -rf {build,dist}/* && python setup.py sdist bdist_wheel
$ twine check dist/*
$ twine upload dist/*
```


## Links and Resources

[Github Repository](https://github.com/adamjakab/BeetsPluginBpmAnalyser)

The PyPi project base is [here](https://pypi.org/project/beets-bpmanalyser/).

[PyPi Publishing docs](https://realpython.com/pypi-publish-python-package/).

[Beets Docs](https://beets.readthedocs.io/en/stable/reference/index.html)

[Beets Wiki](https://github.com/beetbox/beets/wiki)

[Beets forum](https://discourse.beets.io/)
