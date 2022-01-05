# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import configparser
import click
import json
import requests
import sys
from colorama import Fore, Back

OK_GREEN = "\033[92m"
GREY = "\33[90m"
END = "\033[0m"

## Utils that will probably move to where they should be

config = configparser.ConfigParser()
config.read("heroku_guardian/utils/config.ini")
try:
    api_key = config.get("AUTH", "api_key")
except:
    print("No auth token found in config file!")
    sys.exit()


def print_red(string):
    """ Print red text """
    print(f"{Fore.RED}{string}{END}")


def print_purple(string):
    """ Print red text """
    print(f"{Fore.MAGENTA}{string}{END}")


def print_green(string):
    """ Print green text """
    print(f"{Fore.GREEN}{string}{END}")


def convert_red(string):
    """Return red text"""
    return f"{string}"


def convert_green(string):
    """Return green text"""
    return f"{string}"


class heroku_auth:
    def __init__(self, url_extension):
        self.api_key = api_key
        self.url_extension = url_extension

    def get_heroku_api(self):
        base_endpoint = "https://api.heroku.com/"
        headers = {
            "Authorization": "Bearer "+api_key,
            "Accept": "application/vnd.heroku+json; version=3",
        }
        heroku_object = requests.get(
            base_endpoint + self.url_extension, headers=headers
        ).text
        return heroku_object
