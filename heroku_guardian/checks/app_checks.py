# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.resources import apps
from heroku_guardian.utils import utils
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

heroku_addon_providers = config.get("ADDONS", "heroku_addon_providers")
untrusted_plans = config.get("PLANS", "untrusted_plans")
allowed_buildpacks = config.get("BUILDPACKS", "allowed_buildpacks")


def private_space_check(app_name):
    app_info = apps.get_app_info(app_name)
    message = ""
    if app_info.get("space") == None:
        message = utils.convert_red(f"❌  App is not in a space: {app_name}")
    else:
        message = utils.convert_green(
            f"✅  App {app_name} is in a space: " + str(app_info.get("space")["name"])
        )
    return message


def build_pack_check(app_name):
    build_info = apps.get_buildpack(app_name)
    message = ""
    build_stack = ""
    if build_info:
        build_stack = build_info[0]["stack"]
        if build_stack.startswith("heroku"):
            message = utils.convert_green(
                f"✅  Build pack for {app_name} Heroku approved: " + build_stack
            )
        else:
            message = utils.convert_red(
                f"❌  Build pack for {app_name} not Heroku approved: " + build_stack
            )
    return message


def add_on_check(app_name):
    addon_info = apps.get_add_ons(app_name)
    message = ""
    if addon_info:
        for add_on in addon_info:
            add_on_name = add_on["addon_service"]["name"]
            if add_on_name.startswith("heroku"):
                message = utils.convert_green(
                    f"✅  Add on for {app_name} approved: " + add_on_name
                )
            else:
                message = utils.convert_red(
                    f"❌  Add on for {app_name} not approved: " + add_on_name
                )
    return message


def untrusted_plan_check(app_name):
    plan_info = apps.get_add_ons(app_name)
    message = ""
    if plan_info:
        for add_on in plan_info:
            plan_type = add_on["plan"]["name"].split(":")[1]
            if plan_type in untrusted_plans:
                message = utils.convert_red(
                    f"❌  Plan for {app_name} not trusted: " + plan_type
                )
            else:
                message = utils.convert_green(
                    f"✅  Plan for {app_name} trusted: " + plan_type
                )
    return message


def locked_app_check(app_name):
    app_info = apps.get_app_info(app_name)
    message = ""
    if app_info["team"] != None:
        team_app_info = apps.get_team_app_info(app_name)
        if team_app_info["locked"] == True:
            message = utils.convert_green(f"✅  Team app locked for: {app_name}")
    else:
        message = utils.convert_red(f"❌  Team app not locked for: {app_name}")
    return message


def approved_stack_image_check(app_name):
    app_info = apps.get_app_info(app_name)
    message = ""
    if app_info["build_stack"]:
        image = app_info["build_stack"]["name"]
        if image.startswith("heroku"):
            message = utils.convert_green(
                f"✅  Heroku approved stack image used: {app_name}: {image}"
            )
        else:
            message = utils.convert_red(
                f"❌  Not approved stack image used: {app_name}: {image}"
            )
    return message


def maintenence_mode_check(app_name):
    app_info = apps.get_app_info(app_name)
    message = ""
    if app_info["maintenance"] == False:
        message = utils.convert_green(
            f"✅  Heroku app not in maintenance mode: {app_name}"
        )
    else:
        message = utils.convert_red(
            f"❌  Heroku app in maintenance mode, may be unused: {app_name}"
        )
    return message


def domain_name_check(app_name):
    domain_info = apps.get_app_domain(app_name)
    cname_list = []
    message = ""
    for cname in domain_info:
        if cname["cname"] != None:
            cname_list.append(cname["cname"])
    if not cname_list:
        message = utils.convert_red(f"❌  No CNAME assigned for app: {app_name}")
    else:
        message = utils.convert_green(f"✅  CNAME assigned to app: {app_name}")
    return message


def config_vars_check(app_name):
    config_vars = apps.get_app_configvars(app_name)
    message = ""
    if config_vars:
        message = utils.convert_green(f"✅  Config vars assigned to app: {app_name}")
    else:
        message = utils.convert_red(f"❌  Config vars not assigned to app: {app_name}")
    return message


def tls_configuration_check(app_name):
    tls_config = apps.get_tls_verification(app_name)
    message = ""
    if tls_config["enabled"] == True:
        message = utils.convert_green(f"✅  TLS config 1.2+ enabled: {app_name}")
    else:
        message = utils.convert_red(f"❌  TLS config 1.2+ not enabled: {app_name}")
    return message


def internal_routing_check(app_name):
    app_info = apps.get_app_info(app_name)
    message = ""
    if app_info.get("internal_routing") == None:
        message = utils.convert_red(f"❌  App is externally routable: {app_name}")
    else:
        message = utils.convert_green(f"✅  App is not externally routable: {app_name}")
    return message


def perform_app_checks(app):
    app_summary = []
    app_summary.append(
        tuple(
            (
                private_space_check(app),
                "https://devcenter.heroku.com/articles/private-spaces",
            )
        )
    )
    app_summary.append(
        tuple(
            (build_pack_check(app), "https://devcenter.heroku.com/articles/buildpacks")
        )
    )
    app_summary.append(
        tuple(
            (
                internal_routing_check(app),
                "https://devcenter.heroku.com/articles/internal-routing",
            )
        )
    )
    app_summary.append(
        tuple((add_on_check(app), "https://devcenter.heroku.com/articles/add-ons"))
    )
    app_summary.append(
        tuple((untrusted_plan_check(app), "https://www.heroku.com/pricing"))
    )
    app_summary.append(
        tuple(
            (
                locked_app_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#team-app",
            )
        )
    )
    app_summary.append(
        tuple(
            (
                approved_stack_image_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#stack",
            )
        )
    )
    app_summary.append(
        tuple(
            (
                maintenence_mode_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#app",
            )
        )
    )
    app_summary.append(
        tuple(
            (
                domain_name_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#app",
            )
        )
    )
    app_summary.append(
        tuple(
            (
                config_vars_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#config-vars",
            )
        )
    )
    app_summary.append(
        tuple(
            (
                tls_configuration_check(app),
                "https://devcenter.heroku.com/articles/platform-api-reference#app-feature",
            )
        )
    )
    app_summary = [x for x in app_summary if x[0] != ""]
    sorted_summary = sorted(app_summary, key=lambda tup: tup[0])
    return sorted_summary
