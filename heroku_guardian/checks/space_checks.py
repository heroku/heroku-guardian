# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.resources import spaces
from heroku_guardian.utils import utils
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

heroku_addon_providers = config.get("ADDONS", "heroku_addon_providers")
untrusted_plans = config.get("PLANS", "untrusted_plans")
allowed_buildpacks = config.get("BUILDPACKS", "allowed_buildpacks")
allowed_ranges = config.get("RANGES", "allowed_ranges")


def ip_range_check(space):
    space_rule_information = spaces.get_inbound_ruleset(space)
    ip_range = []
    summary_list = []
    for rule in space_rule_information["rules"]:
        ip_range.append(rule["source"])
    for ip in ip_range:
        if ip not in allowed_ranges:
            summary_list.append(
                utils.convert_red(
                    f"❌  IP Range {ip} is not in an allowed source IP range."
                )
            )
        else:
            summary_list.append(
                utils.convert_green(f"✅  IP Range {ip} is an allowed source IP range.")
            )
    return summary_list


def perform_space_checks(space):
    utils.print_purple(f"Performing health checks on {space}")
    space_summary = ip_range_check(space)
    sorted_summary = sorted(space_summary, key=lambda tup: tup[0])
    return sorted_summary
