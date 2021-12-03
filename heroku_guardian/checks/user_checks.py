# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
from heroku_guardian.resources import users
from heroku_guardian.utils import utils
import configparser

config = configparser.ConfigParser()
config.read("heroku_guardian/utils/config.ini")

heroku_addon_providers = config.get("ADDONS", "heroku_addon_providers")
untrusted_plans = config.get("PLANS", "untrusted_plans")
allowed_buildpacks = config.get("BUILDPACKS", "allowed_buildpacks")
allowed_ranges = config.get("RANGES", "allowed_ranges")
company_email = config.get("USER", "email_domain")


def check_email():
    user_info = users.get_user_info()
    summary = ""
    if user_info["email"]:
        summary = utils.convert_green(f"✅  User email set correctly.")
    else:
        summary = utils.convert_red(f"❌  User email is not set")
    return summary


def check_sfdc_email():
    user_info = users.get_user_info()
    user_email = user_info["email"]
    summary = ""
    if user_email.endswith(company_email):
        summary = utils.convert_green(f"✅  Approved email domain being used.")
    else:
        summary = utils.convert_red(f"❌  Non-approved email domain is being used: {user_email}")
    return summary


def check_mfa():
    user_info = users.get_user_info()
    summary = ""
    if user_info["two_factor_authentication"] == True:
        summary = utils.convert_green(f"✅  User has MFA enabled.")
    else:
        summary = utils.convert_red(f"❌  User does not have MFA enabled.")
    return summary

def check_sso():
    user_info = users.get_user_info()
    summary = ""
    if user_info["federated"] == True:
        summary = utils.convert_green(f"✅  User is using federated login.")
    else:
        summary = utils.convert_red(f"❌  User is not using federated login.")
    return summary


def check_sso_preferred():
    user_info = users.get_user_info()
    summary = ""
    if (
        user_info["federated"] == False
        and user_info["two_factor_authentication"] == True
    ):
        summary = utils.convert_green(f"❌  SSO not is preferred.")
    return summary


def perform_user_checks():
    email = users.get_user_info()["email"]
    utils.print_purple(f"Performing health checks for user {email}")
    user_summary = []
    user_summary.append(check_email())
    user_summary.append(check_sfdc_email())
    user_summary.append(check_sso())
    user_summary.append(check_mfa())
    user_summary.append(check_sso_preferred())
    user_summary = list(filter(None, user_summary))
    sorted_summary = sorted(user_summary, key=lambda tup: tup[0])
    return sorted_summary
