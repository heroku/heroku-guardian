# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.utils import utils
import json


def get_user_info():
    user_info = json.loads(utils.heroku_auth(f"account").get_heroku_api())
    return user_info