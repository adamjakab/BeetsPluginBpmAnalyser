#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 12:35 PM
#  License: See LICENSE.txt
#

from test.helper import TestHelper, Assertions, PLUGIN_NAME, PLUGIN_SHORT_DESCRIPTION, capture_stdout


# Minimal sanityt tests
class SanityTest(TestHelper, Assertions):

    # Test that when running the application, the plugin shows up (name and short description)
    def test_application(self):
        with capture_stdout() as out:
            self.runcli()

        self.assertIn(PLUGIN_NAME, out.getvalue())
        self.assertIn(PLUGIN_SHORT_DESCRIPTION, out.getvalue())

    # Test that the plugin shows up in the list of loaded plugins 
    def test_application_plugin_list(self):
        with capture_stdout() as out:
            self.runcli("version")

        self.assertIn("plugins: {0}".format(PLUGIN_NAME), out.getvalue())

    def test_plugin(self):
        self.runcli(PLUGIN_NAME)
