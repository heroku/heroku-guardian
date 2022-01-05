# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
### Application specific checks
from heroku_guardian.resources import apps
from heroku_guardian.resources import spaces
from heroku_guardian.checks import app_checks
from heroku_guardian.utils import utils
import click
import json


@click.command(short_help="Perform app security checks within Heroku")
@click.option(
    "--app-name",
    "-a",
    type=str,
    required=False,
    help="App name that you would like to perform security checks for",
)
@click.option(
    "--space-name",
    "-s",
    type=str,
    required=False,
    help="Space that you would like to perform security checks for",
)
@click.option(
    "--links",
    "-l",
    is_flag=True,
    type=bool,
    required=False,
    help="Findings with links to Heroku API documentation",
)
@click.option(
    "--json-output",
    "-j",
    is_flag=True,
    type=bool,
    required=False,
    help="Output JSON findings",
)
def app(app_name=str, space_name=str, links=bool, json_output=bool):
    findings = {}
    if app_name:
        if json_output:
            json_list = []
            finding_list = app_checks.perform_app_checks(app_name)
            for item in finding_list:
                json_list.append(item[0].split("  ", 1)[1])
                findings[app_name] = json_list
            print(json.dumps(findings, indent=4, sort_keys=True))
        else:
            for item in app_checks.perform_app_checks(app_name):
                if links:
                    print(f"{item[0]}:{item[1]}")
                else:
                    print(f"{item[0]}")
    elif space_name:
        if json_output:
            space_list = apps.get_space_app_list(space_name)
            for app in space_list:
                json_list = []
                finding_list = app_checks.perform_app_checks(app)
                for item in finding_list:
                    json_list.append(item[0].split("  ", 1)[1])
                    findings[app] = json_list
            print(json.dumps(findings, indent=4, sort_keys=True))
        else:
            utils.print_purple(f"Performing health checks on apps in {space_name}")
            space_list = apps.get_space_app_list(space_name)
            print(space_list)
            for app in space_list:
                utils.print_purple(app)
                for item in app_checks.perform_app_checks(app):
                    if links:
                        print(f"{item[0]:<80}{item[1]:}")
                    else:
                        print(f"{item[0]}")
    else:
        if json_output:
            for app in apps.get_user_app_list():
                json_list = []
                finding_list = app_checks.perform_app_checks(app)
                for item in finding_list:
                    json_list.append(item[0].split("  ", 1)[1])
                    findings[app] = json_list
            print(json.dumps(findings, indent=4, sort_keys=True))
        else:
            utils.print_purple(f"Performing health checks on apps")
            for app in apps.get_user_app_list():
                utils.print_purple(app)
                for item in app_checks.perform_app_checks(app):
                    if links:
                        print(f"{item[0]:<80}{item[1]:}")
                    else:
                        print(f"{item[0]}")
