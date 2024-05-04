#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 10:50 PM
#  License: See LICENSE.txt

import logging

from beets.plugins import BeetsPlugin
from beetsplug.bpmanalyser.command import BpmAnalyserCommand

log = logging.getLogger('beets.bpmanalyser')


class BpmAnalyserPlugin(BeetsPlugin):

    def __init__(self):
        super(BpmAnalyserPlugin, self).__init__()
        self.config.add({
            'auto': False,
            'dry-run': False,
            'write': True,
            'threads': "AUTO",
            'force': False,
            'quiet': False
        })

        # On-import analysis.
        if self.config['auto']:
            self.import_stages = [self.imported]

    def commands(self):
        return [BpmAnalyserCommand(self.config)]

    def imported(self, session, task):
        # Add BPM for imported items.
        for item in task.imported_items():
            if not self.config['force'] and item['bpm'] != 0:
                item_path = item.get("path").decode("utf-8")
                log.debug("Skipping item with existing BPM[{0}]...".format(item_path))
                return
            else:
                BpmAnalyserCommand(self.config).analyse(item)
