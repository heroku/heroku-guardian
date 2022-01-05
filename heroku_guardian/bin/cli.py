#! /usr/bin/env python
# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""
    Heroku guardian is a tool used to validate that your deployment, spaces, and user configuration are secure.
"""
import click
from heroku_guardian import command
from heroku_guardian.bin.version import __version__


@click.group()
@click.version_option(version=__version__)
def heroku_guardian():
    """
    Heroku guardian is a tool used to validate that your deployment, spaces, and user configuration are secure.
    """


heroku_guardian.add_command(command.app.app)
heroku_guardian.add_command(command.space.space)
heroku_guardian.add_command(command.user.user)


def main():
    """ Heroku guardian is a tool used to validate that your deployment, spaces, and user configuration are secure. """
    heroku_guardian()


if __name__ == "__main__":
    heroku_guardian()
