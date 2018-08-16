#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""Jenkins

Usage:
    yorktown jenkins --showconfig [-j JOBNAME, -u USER, --pass PASSWORD]
    yorktown jenkins --build [-j JOBNAME, -p PARAMS]
    yorktown jenkins -h

Arguments:
    JOBNAME                           Name of Jenkins job
    PARAMS                            Parameters for the job
    USERNAME                          Username
    PASSWORD                          Password

Options:
    -h                                show this message
    -j JOBNAME, --jobname JOBNAME     job to run
    -p PARAMS, --params PARAMS        job params as a json string
    -u USER, --user USER              username
    --pass PASSWORD                   password
"""

from docopt import docopt
from lib.utils import get_arg_option
from yorktown.lib.utils import AnsiColor as color
from yorktown.lib.utils import print_arguements
from yorktown.lib.libjenkins import Jenkins
import sys
import os
import logging
import json
logger = logging.getLogger(__name__)

CONSTANTS = {
    "main": {
        "url": "https://jenkins.localdomain",
        "username": "svc-account-example",
        "password": "example_378D00509BD04834BCC40538F48E7EB7",
    }
}

class HudsonCommand(object):
    """Jenkins
    Argument:
        args (dict): A dictionary returned by docopt after CLI is parsed
    """

    def __init__(self, args):
        self.args = args
        print_arguements(args)

    def showconfig(self):
        """
        print xml config of a job
        """
        job = self.args['--jobname']
        user = self.args['--user']
        passw = self.args['--pass']
        j = Jenkins()
        jenkins_kwargs = CONSTANTS['main']
        j.show_config(jenkins_class_args=jenkins_kwargs, job=job, user=user, passw=passw)

    def build(self):
        """
        build command
        """
        job = self.args['--jobname']
        params = self.args['--params']
        try:
            # will fail if json does not compute
            if params:
                json.loads(params)
        except ValueError as e:
            logger.error("Exception! Arguement --params: {}!".format(e))
            exit(1)
        j = Jenkins()
        logger.info("{name}: parameters {p}".format(name=job, p=params))
        jenkins_kwargs = CONSTANTS['main']
        if j.build(jenkins_class_args=jenkins_kwargs, job=job, params=params):
            logger.info("OK")
        else:
            logger.info("FAIL")
            exit(1)


def main():
    """Parse the CLI"""
    arguments = docopt(__doc__)

    cmd = HudsonCommand(arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
