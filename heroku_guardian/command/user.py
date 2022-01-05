# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
### User specific checks
from heroku_guardian.resources import users
from heroku_guardian.checks import user_checks
from heroku_guardian.utils import utils
import click
import json


@click.command(short_help="Perform user security checks within Heroku")
@click.option(
    "--json-output",
    "-j",
    is_flag=True,
    type=bool,
    required=False,
    help="User check with JSON output",
)
def user(json_output=bool):
    if json_output:
        json_list = []
        checks = user_checks.perform_user_checks()
        for item in checks:
            json_list.append(item.split("  ", 1)[1])
        print(json.dumps(json_list, indent=4, sort_keys=True))
    else:
        checks = user_checks.perform_user_checks()
        for item in checks:
            print(item)
