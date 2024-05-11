#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/23/20, 10:50 PM
#  License: See LICENSE.txt

import logging
import os

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
        BpmAnalyserCommand(self.config).execute_task_on_items(task.imported_items())
        
        # Because of this pydub issue(https://github.com/jiaaro/pydub/issues/503) the below is necessary for now
        # to regain console input (can also use reset) - not sure if Windows is affected
        if os.name != 'nt':
            os.system('stty echo')
