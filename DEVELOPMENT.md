# Development Notes 

## General
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



## Deployment of a new version

I guess this is mostly for me:

```shell script
$ bumpversion --current-version 1.0.0 minor setup.py
$ rm -rf {build,dist}/* && python setup.py sdist bdist_wheel
$ twine check dist/*
$ twine upload dist/*
```


## Links and Resources

[Girhub Repository](https://github.com/adamjakab/BeetsPluginBpmAnalyser)

The PyPi project base is [here](https://pypi.org/project/beets-bpmanalyser/).

[PyPi Publishing docs](https://realpython.com/pypi-publish-python-package/).

