#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/18/20, 12:31 AM
#  License: See LICENSE.txt
#
# References: https://docs.python.org/3/library/unittest.html
#
import json
import os
import shutil
import sys
import tempfile
from contextlib import contextmanager
from random import randint
from unittest import TestCase

import beets
import six
import yaml
from beets import logging
from beets import plugins
from beets import ui
from beets import util
from beets.library import Item
# from beets.mediafile import MediaFile
from beets.util import (
    MoveOperation,
    syspath,
    bytestring_path,
    displayable_path,
)
from beets.util.confit import Subview, Dumper
from six import StringIO

from beetsplug import bpmanalyser

logging.getLogger('beets').propagate = True

# Values
PLUGIN_NAME = 'bpmanalyser'
PLUGIN_SHORT_DESCRIPTION = 'analyse your songs for tempo and write it into the bpm tag'


class LogCapture(logging.Handler):

    def __init__(self):
        super(LogCapture, self).__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(six.text_type(record.msg))


@contextmanager
def capture_log(logger='beets', suppress_output=True):
    capture = LogCapture()
    log = logging.getLogger(logger)
    log.propagate = True
    if suppress_output:
        # Is this too violent?
        log.handlers = []
    log.addHandler(capture)
    try:
        yield capture.messages
    finally:
        log.removeHandler(capture)


@contextmanager
def capture_stdout(suppress_output=True):
    """Save stdout in a StringIO.
    >>> with capture_stdout() as output:
    ...     print('spam')
    ...
    >>> output.getvalue()
    'spam'
    """
    org = sys.stdout
    sys.stdout = capture = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = org
        # if not suppress_output:
        print(capture.getvalue())


@contextmanager
def control_stdin(userinput=None):
    """Sends ``input`` to stdin.
    >>> with control_stdin('yes'):
    ...     input()
    'yes'
    """
    org = sys.stdin
    sys.stdin = StringIO(userinput)
    try:
        yield sys.stdin
    finally:
        sys.stdin = org


def _convert_args(args):
    """Convert args to strings
    """
    for i, elem in enumerate(args):
        if isinstance(elem, bytes):
            args[i] = elem.decode(util.arg_encoding())

    return args


class Assertions(object):
    def assertIsFile(self: TestCase, path):
        self.assertTrue(os.path.isfile(syspath(path)),
                        msg=u'Path is not a file: {0}'.format(displayable_path(path)))


class TestHelper(TestCase, Assertions):
    _test_config_dir_ = os.path.join(bytestring_path(os.path.dirname(__file__)), b'config')
    _test_fixture_dir = os.path.join(bytestring_path(os.path.dirname(__file__)), b'fixtures')
    _test_target_dir = bytestring_path("/tmp/beets-bpmanalyser")

    def setUp(self):
        """Setup required for running test. Must be called before running any tests.
        """
        self.reset_beets(config_file=b"empty.yml")

    def tearDown(self):
        self.teardown_beets()

    def reset_beets(self, config_file: bytes):
        self.teardown_beets()
        plugins._classes = {bpmanalyser.BpmAnalyserPlugin}
        self._setup_beets(config_file)

    def _setup_beets(self, config_file: bytes):
        self.addCleanup(self.teardown_beets)
        os.environ['BEETSDIR'] = self.mkdtemp()

        self.config = beets.config
        self.config.clear()

        # add user configuration
        config_file = format(os.path.join(self._test_config_dir_, config_file).decode())
        shutil.copyfile(config_file, self.config.user_config_path())
        self.config.read()

        self.config['plugins'] = []
        self.config['verbose'] = True
        self.config['ui']['color'] = False
        self.config['threaded'] = False
        self.config['import']['copy'] = False

        os.makedirs(self._test_target_dir, exist_ok=True)

        libdir = self.mkdtemp()
        self.config['directory'] = libdir
        self.libdir = bytestring_path(libdir)

        self.lib = beets.library.Library(':memory:', self.libdir)

        # This will initialize (create instance) of the plugins
        plugins.find_plugins()

    def teardown_beets(self):
        self.unload_plugins()

        shutil.rmtree(self._test_target_dir, ignore_errors=True)

        if hasattr(self, '_tempdirs'):
            for tempdir in self._tempdirs:
                if os.path.exists(tempdir):
                    shutil.rmtree(syspath(tempdir), ignore_errors=True)
        self._tempdirs = []

        if hasattr(self, 'lib'):
            if hasattr(self.lib, '_connections'):
                del self.lib._connections

        if 'BEETSDIR' in os.environ:
            del os.environ['BEETSDIR']

        if hasattr(self, 'config'):
            self.config.clear()

        # beets.config.read(user=False, defaults=True)

    def mkdtemp(self):
        # This return a str path, i.e. Unicode on Python 3. We need this in
        # order to put paths into the configuration.
        path = tempfile.mkdtemp()
        self._tempdirs.append(path)
        return path

    @staticmethod
    def unload_plugins():
        for plugin in plugins._classes:
            plugin.listeners = None
            plugins._classes = set()
            plugins._instances = {}

    def runcli(self, *args):
        # TODO mock stdin
        with capture_stdout() as out:
            try:
                ui._raw_main(_convert_args(list(args)), self.lib)
            except ui.UserError as u:
                # TODO remove this and handle exceptions in tests
                print(u.args[0])
        return out.getvalue()

    def lib_path(self, path):
        return os.path.join(self.libdir, path.replace(b'/', bytestring_path(os.sep)))

    @staticmethod
    def _dump_config(cfg: Subview):
        # print(json.dumps(cfg.get(), indent=4, sort_keys=False))
        flat = cfg.flatten()
        print(yaml.dump(flat, Dumper=Dumper, default_flow_style=None, indent=2, width=1000))


