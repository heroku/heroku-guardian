# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
### Space specific checks
from heroku_guardian.resources import spaces
from heroku_guardian.checks import space_checks
from heroku_guardian.utils import utils
import click
import json


@click.command(short_help="Perform space security checks within Heroku")
@click.option(
    "--space-name",
    "-s",
    type=str,
    required=False,
    help="Space name that you would like to perform security checks for",
)
@click.option(
    "--json-output",
    "-j",
    type=bool,
    is_flag=True,
    required=False,
    default=False,
    help="Space check with JSON output",
)
def space(json_output=bool, space_name=str):
    findings = {}
    if space_name:
        if json_output:
            json_list = []
            checks = space_checks.perform_space_checks(space_name)
            for item in checks:
                json_list.append(item.split("  ", 1)[1])
                findings = json_list
            print(json.dumps(findings, indent=4, sort_keys=True))
        else:
            checks = space_checks.perform_space_checks(space_name)
            for item in checks:
                print(item)
    else:
        if json_output:
            space_list = spaces.get_space_list()
            for space in space_list:
                json_list = []
                checks = space_checks.perform_space_checks(space)
                for item in checks:
                    json_list.append(item.split("  ", 1)[1])
                    findings[space] = json_list
            print(json.dumps(findings, indent=4, sort_keys=True))
        else:
            space_list = spaces.get_space_list()
            for space in space_list:
                checks = space_checks.perform_space_checks(space)
                for item in checks:
                    print(item)
