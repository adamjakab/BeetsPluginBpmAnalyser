#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 10:50 PM
#  License: See LICENSE.txt


from beets.plugins import BeetsPlugin
from beets.util import cpu_count

from beetsplug.bpmanalyser.command import BpmAnayserCommand


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
