#!/usr/bin/env python
# Copyright (c) 2022, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import sys
import os
import logging
from invoke import task, Collection

BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "heroku_guardian", "bin", "cli.py"))
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, "heroku_guardian")
    )
)

# Create the necessary collections (namespaces)
ns = Collection()

test = Collection("test")
ns.add_collection(test)

@task
def app(c):
    c.run(f"echo 'App security checks'")
    c.run(f"{BIN} app", pty=True)

def space(c):
    c.run(f"echo 'Space security checks'")
    c.run(f"{BIN} space", pty=True)

def user(c):
    c.run(f"echo 'User security checks'")
    c.run(f"{BIN} user", pty=True)


test.add_task(app, "app")
test.add_task(app, "space")
test.add_task(app, "user")
