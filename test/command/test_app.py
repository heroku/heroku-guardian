# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import json
import unittest
import warnings
from click.testing import CliRunner
from heroku_guardian.command.app import app


class AppSecurityChecksClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

    def test_app_security_checks_help(self):
        """ apps with help will exit 0 """
        result = self.runner.invoke(app, ["--help"])
        self.assertTrue(result.exit_code == 0)
