# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import json
import unittest
import warnings
from click.testing import CliRunner
from heroku_guardian.command.user import user


class UserSecurityChecksClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)

    def test_space_security_checks_help(self):
        """ user with help will exit 0 """
        result = self.runner.invoke(user, ["--help"])
        self.assertTrue(result.exit_code == 0)
