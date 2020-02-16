#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/16/20, 10:50 AM
#  License: See LICENSE.txt
#


import os
import logging
from optparse import OptionParser

# import beets
from beets import config as beets_global_config
from beets.library import Library as BeatsLibrary
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand, decargs
from beets.util import cpu_count
from subprocess import Popen, PIPE
from concurrent import futures

# Module methods
log = logging.getLogger('beets.bpmanalyser')


# Classes ###
class BpmAnalyserPlugin(BeetsPlugin):
    def __init__(self):
        super(BpmAnalyserPlugin, self).__init__()
        self.config.add({
            'auto': False,
            'dry-run': False,
            'write': True,
            'threads': cpu_count(),
            'force': False,
            'quiet': False
        })

    def commands(self):
        return [BpmAnayserCommand(self.config)]


class BpmAnayserCommand(Subcommand):
    config = None
    lib = None
    query = None
    parser = None

    cfg_auto = False
    cfg_dry_run = False
    cfg_write = True
    cfg_threads = 1
    cfg_force = False
    cfg_quiet = False

    analyser_script_path = None

    def __init__(self, cfg):
        self.config = cfg.flatten()

        self.cfg_auto = self.config.get("auto")
        self.cfg_dry_run = self.config.get("dry-run")
        self.cfg_write = self.config.get("write")
        self.cfg_threads = self.config.get("threads")
        self.cfg_force = self.config.get("force")
        self.cfg_quiet = self.config.get("quiet")

        self.analyser_script_path = os.path.dirname(os.path.realpath(__file__)) + "/get_song_bpm.py"

        self.parser = OptionParser(usage='%prog training_name [options] [QUERY...]')

        self.parser.add_option(
            '-d', '--dry-run',
            action='store_true', dest='dryrun', default=self.cfg_dry_run,
            help=u'[default: {}] display the bpm values but do not update the library items'.format(self.cfg_dry_run)
        )

        self.parser.add_option(
            '-w', '--write',
            action='store_true', dest='write', default=self.cfg_write,
            help=u'[default: {}] write the bpm values to the media files'.format(self.cfg_write)
        )

        self.parser.add_option(
            '-t', '--threads',
            action='store', dest='threads', default=self.cfg_threads,
            help=u'[default: {}] the number of threads to run in parallel'.format(self.cfg_threads)
        )

        self.parser.add_option(
            '-f', '--force',
            action='store_true', dest='force', default=self.cfg_force,
            help=u'[default: {}] force analysis of items with non-zero bpm values'.format(self.cfg_force)
        )

        self.parser.add_option(
            '-q', '--quiet',
            action='store_true', dest='quiet', default=self.cfg_quiet,
            help=u'[default: {}] mute all output'.format(self.cfg_quiet)
        )

        # Keep this at the end
        super(BpmAnayserCommand, self).__init__(
            parser=self.parser,
            name='bpmanalyser',
            help=u'analyse your songs for tempo and write it into the bpm tag'
        )

    def func(self, lib: BeatsLibrary, options, arguments):
        self.cfg_dry_run = options.dryrun
        self.cfg_write = options.write
        self.cfg_threads = options.threads
        self.cfg_force = options.force
        self.cfg_quiet = options.quiet

        self.lib = lib
        self.query = decargs(arguments)

        self.analyse_songs()

    def analyse_songs(self):
        # Setup the query
        query = self.query
        if not self.cfg_force:
            query_element = "bpm:0"
            query.append(query_element)

        # Get the library items
        # @todo: implement a limit option so that user can decide to do only a imited number of items per run
        items = self.lib.items(self.query)

        def analyse(item):
            item_path = item.get("path").decode("utf-8")
            log.debug("Analysing[{0}]...".format(item_path))

            bpm = int(self.get_bpm_from_analyser_script(item_path))

            self._say("Song[{0}] bpm: {1}".format(item_path, bpm))

            if not self.cfg_dry_run:
                if bpm != 0:
                    item['bpm'] = bpm
                    if self.cfg_write:
                        item.try_write()
                    item.store()

        self.execute_on_items(items, analyse, msg='Analysing tempo...')

    def get_bpm_from_analyser_script(self, item_path):
        proc = Popen([self.analyser_script_path, item_path], stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        bpm = int(stdout.decode("utf-8"))
        # @todo: log error messages from external script
        # self._say("O: {}".format(stdout.decode("utf-8")))
        # self._say("E: {}".format(stderr.decode("utf-8")))
        return bpm

    def execute_on_items(self, items, func, msg=None):
        total = len(items)
        finished = 0
        with futures.ThreadPoolExecutor(max_workers=self.cfg_threads) as e:
            for _ in e.map(func, items):
                finished += 1
                # @create and show a progress bar (--progress-only option)

    def _say(self, msg):
        if not self.cfg_quiet:
            log.info(msg)
        else:
            log.debug(msg)
