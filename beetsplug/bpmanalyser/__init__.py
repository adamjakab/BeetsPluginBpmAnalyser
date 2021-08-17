#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 10:50 PM
#  License: See LICENSE.txt


from beets.plugins import BeetsPlugin
from beets.util import cpu_count
from beetsplug.bpmanalyser.command import BpmAnalyserCommand


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

        # On-import analysis.
        if self.config['auto']:
            self.import_stages = [self.imported]

    def commands(self):
        return [BpmAnalyserCommand(self.config)]

    def imported(self, session, task):
        # Add BPM for imported items.
        for item in task.imported_items():
            BpmAnalyserCommand(self.config).analyse(item)
