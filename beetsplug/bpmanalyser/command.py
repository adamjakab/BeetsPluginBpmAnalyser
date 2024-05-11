#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 10:53 PM
#  License: See LICENSE.txt

import os
import sys
import multiprocessing
import json
import logging
import concurrent.futures as cf

from optparse import OptionParser
from subprocess import PIPE, Popen

from beets.library import Library as BeatsLibrary, Item
from beets.ui import Subcommand, decargs

# Module methods
log = logging.getLogger('beets.bpmanalyser')

# Constants
__FRAME_RATE__ = 44100


class BpmAnalyserCommand(Subcommand):
    config = None
    lib = None
    query = None
    parser = None

    cfg_dry_run = False
    cfg_write = True
    cfg_threads = "AUTO"
    cfg_force = False
    cfg_quiet = False

    analyser_script_path = None

    #
    # Initialize the plugin
    #
    def __init__(self, cfg):
        self.config = cfg.flatten()

        self.cfg_dry_run = self.config.get("dry-run")
        self.cfg_write = self.config.get("write")
        self.cfg_threads = self.config.get("threads")
        self.cfg_force = self.config.get("force")
        self.cfg_version = False
        self.cfg_quiet = self.config.get("quiet")

        self.parser = OptionParser(usage='%prog [options] [QUERY...]')

        self.parser.add_option(
            '-d', '--dry-run',
            action='store_true', dest='dryrun', default=self.cfg_dry_run,
            help=u'[default: {}] display the bpm values but do not update the '
                 u'library items'.format(
                self.cfg_dry_run)
        )

        self.parser.add_option(
            '-w', '--write',
            action='store_true', dest='write', default=self.cfg_write,
            help=u'[default: {}] write the bpm values to the media '
                 u'files'.format(
                self.cfg_write)
        )

        self.parser.add_option(
            '-t', '--threads',
            action='store', dest='threads', type='string',
            default=self.cfg_threads,
            help=u'[default: {}] the number of threads to run in '
                 u'parallel'.format(
                self.cfg_threads)
        )

        self.parser.add_option(
            '-f', '--force',
            action='store_true', dest='force', default=self.cfg_force,
            help=u'[default: {}] force analysis of items with non-zero bpm '
                 u'values'.format(
                self.cfg_force)
        )

        self.parser.add_option(
            '-q', '--quiet',
            action='store_true', dest='quiet', default=self.cfg_quiet,
            help=u'[default: {}] mute all output'.format(self.cfg_quiet)
        )

        self.parser.add_option(
            '-v', '--version',
            action='store_true', dest='version', default=self.cfg_version,
            help=u'show plugin version'
        )
        
        # set up the analyser script path
        module_path = os.path.dirname(__file__)
        self.analyser_script_path = os.path.join(module_path, "analyser.py")
        if not os.path.isfile(self.analyser_script_path):
            raise FileNotFoundError("Analyser script not found!")
        # log.debug("External analyser script path: {}".format(self.analyser_script_path))

        # Keep this at the end
        super(BpmAnalyserCommand, self).__init__(
            parser=self.parser,
            name='bpmanalyser',
            help=u'analyse your songs for tempo and write it into the bpm tag'
        )

    #
    # The main entry function for running the extension
    #
    def func(self, lib: BeatsLibrary, options, arguments):
        self.cfg_dry_run = options.dryrun
        self.cfg_write = options.write
        self.cfg_threads = options.threads
        self.cfg_force = options.force
        self.cfg_version = options.version
        self.cfg_quiet = options.quiet

        self.lib = lib
        self.query = decargs(arguments)

        if options.version:
            self.show_version_information()
            return

        self.analyse_songs()
        
        # Because of this pydub issue(https://github.com/jiaaro/pydub/issues/503) the below is necessary for now
        # to regain console input (can also use reset) - not sure if Windows is affected
        if os.name != 'nt':
            os.system('stty echo')
    
    #
    # Setup and trigger analysis
    #
    def analyse_songs(self):
        # self.find_analyser_script()

        # Setup the query
        query = self.query
        if not self.cfg_force:
            query_element = "bpm:0"
            query.append(query_element)

        # Get the library items
        # @TODO: implement a limit option so that user can decide to do only a limited number of items per run
        items = self.lib.items(self.query)

        self.execute_task_on_items(items)
    
    #
    # Pass all items to multithread Executor
    #
    def execute_task_on_items(self, items):
        total = len(items)
        taskRef = self.runAnalyser
        finished = 0
        
        max_workers = 1
        if str(self.cfg_threads).isnumeric():
            max_workers = int(self.cfg_threads)
        elif self.cfg_threads == "AUTO":
            max_workers = round(multiprocessing.cpu_count() * 0.75)
            
        self._say("BpmAnalyser exec threads: {}".format(max_workers))
        
        # @TODO: create and show a progress bar (--progress-only option)
        with cf.ThreadPoolExecutor(max_workers) as executor:
            for result in executor.map(taskRef, items):
                finished += 1
            
        self._say("Done.")
    
    #
    # Run the external analyser script on a single item
    #
    def runAnalyser(self, item: Item):
        item_path = item.get("path").decode("utf-8")
        log.debug("Analysing[{0}]...".format(item_path))
        
        proc = Popen([sys.executable, self.analyser_script_path, item_path],
                     stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        # By default assume unknown error
        error = True
        message = "Unknown error!"
        bpm = 0
        
        # On successful execution script should output a json
        try:
            resp = json.loads(stdout)
            error = resp["error"]
            message = resp["message"]
            bpm = resp["bpm"]
        except Exception:
            message = message + " Unparsable response."
            
        if (proc.returncode != 0 or error == True):
            log.error("Error({}): {}".format(proc.returncode, message))
            return False
        
        if bpm != 0:
            if not self.cfg_dry_run:
                item['bpm'] = bpm
                if self.cfg_write:
                    item.try_write()
                item.store()
                self._say("Bpm[{}]: {}".format(bpm, item_path))
            else:
                self._say("Bpm[DRY-MODE][{}]: {}".format(bpm, item_path))
        else:
            log.error("Error: bpm=0 was found. Not setting!")

    # Plugin version Information
    def show_version_information(self):
        from beetsplug.bpmanalyser.version import __version__
        self._say(
            "Bpm Analyser(beets-bpmanalyser) plugin for Beets: v{0}".format(
                __version__))
    
    # Say something (if not in quiet mode)
    def _say(self, msg):
        if not self.cfg_quiet:
            log.info(msg)
        else:
            log.debug(msg)
