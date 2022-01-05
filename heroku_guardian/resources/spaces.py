# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.utils import utils
import json


def get_space_info(space):
    space_info = json.loads(utils.heroku_auth(f"spaces/{space}").get_heroku_api())
    return space_info


def get_inbound_ruleset(space):
    space_rules = json.loads(
        utils.heroku_auth(f"spaces/{space}/inbound-ruleset").get_heroku_api()
    )
    return space_rules


def get_space_list():
    space_json = json.loads(utils.heroku_auth(f"spaces").get_heroku_api())
    space_list = []
    for space in space_json:
        space_list.append(space["name"])
    return space_list
