# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.utils import utils
from heroku_guardian.resources import users
import json


def get_tls_verification(app_name):
    json_of_tls = json.loads(
        utils.heroku_auth(
            f"apps/{app_name}/features/spaces-tls-salesforce"
        ).get_heroku_api()
    )
    return json_of_tls


def get_app_configvars(app_name):
    json_of_configvars = json.loads(
        utils.heroku_auth(f"apps/{app_name}/config-vars").get_heroku_api()
    )
    boolean_of_configvars = False
    if json_of_configvars:
        boolean_of_configvars = True
    return boolean_of_configvars


def get_app_domain(app_name):
    json_of_domain = json.loads(
        utils.heroku_auth(f"apps/{app_name}/domains").get_heroku_api()
    )
    return json_of_domain


def get_buildpack(app_name):
    json_of_buildpack = json.loads(
        utils.heroku_auth(f"apps/{app_name}/builds").get_heroku_api()
    )
    return json_of_buildpack


def get_add_ons(app_name):
    json_of_addons = json.loads(
        utils.heroku_auth(f"apps/{app_name}/addons").get_heroku_api()
    )
    return json_of_addons


def get_user_app_list():
    email = users.get_user_info()["email"]
    json_of_apps = json.loads(utils.heroku_auth(f"users/{email}/apps").get_heroku_api())
    app_list = []
    for each_app in json_of_apps:
        app_list.append(each_app.get("name"))
    return app_list


def get_team_app_info(app_name):
    json_team_app_info = json.loads(
        utils.heroku_auth(f"teams/apps/{app_name}").get_heroku_api()
    )
    return json_team_app_info


def get_team_app_list(team):
    json_of_apps = utils.heroku_auth(f"teams/{team}/apps").get_heroku_api()
    team_app_list = []
    for each_app in json_of_apps:
        team_app_list.append(each_app.get("name"))
    return team_app_list


def get_space_app_list(space):
    json_of_apps = json.loads(
        utils.heroku_auth(f"spaces/{space}/topology").get_heroku_api()
    )
    id_list = []
    space_app_list = []
    for apps in json_of_apps["apps"]:
        id_list.append(apps.get("id"))
    for id in id_list:
        space_app_list.append(
            json.loads(utils.heroku_auth(f"apps/" + id).get_heroku_api())["name"]
        )
    return space_app_list


def get_app_info(app_name):
    app_information = json.loads(utils.heroku_auth(f"apps/{app_name}").get_heroku_api())
    return app_information