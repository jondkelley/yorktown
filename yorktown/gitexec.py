#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""Execute a remote command from git

Usage:
    yorktown gitexec --run [-r REPOSITORY_URL, -b BRANCH, -t TAG, -i INTERPRETER, -c COMMAND, -a ARGS, -e ENVIRONMENT]
    yorktown gitexec -h

Arguments:
    REPOSITORY_URL                                     repository URL
                                                       i.e. (git@github.com:organization/{repo})
                                                       i.e. (https://{git_token}:x-oauth-basic@github.com/organization/{repo})
    BRANCH                                             git branch to checkout
    TAG                                                git tag to checkout
    COMMAND                                            command to run from local git checkout
    ARGS                                               arguements to pass to command
    ENVIRONMENT                                        environment variables to export

Options:
    -h                                                 show this message
    -r REPOSITORY_URL, --repo REPOSITORY_URL           repository URL
    -b BRANCH, --branch BRANCH                         git branch to checkout (use tags/name for a tag)
    -t TAG, --tag TAG                                  git tag to checkout
    -i INTERPRETER, --interpreter INTERPRETER          optional interpreter i.e. python, bash, php
    -c COMMAND, --command COMMAND                      command to run under branch
    -a ARGS, --arguements ARGS                         arguements to pass as a string (use quotes) i.e. ("-i -o gcc.so")
    -e ENVIRONMENT, --environment ENVIRONMENT          environment variables to export i.e. (HOME=/,CWD=/)

"""

from docopt import docopt
from lib.utils import get_arg_option
from yorktown.lib.utils import print_arguements, shell_command
from yorktown.lib.utils import AnsiColor as color
from yorktown.lib.libgit import GitCrud
from yorktown.lib.utils import shell_command

import sys
import os
import logging
logger = logging.getLogger(__name__)

class GitExcCommand(object):
    """GitExc
    Argument:
        args (dict): A dictionary returned by docopt after CLI is parsed
    """
    def __init__(self, args):
        self.args = args
        print_arguements(args)

    def run(self):
        """
        runs a command from a git repository / branch
        """
        repo = self.args['--repo']
        logger.info("Cloning repository: {}".format(repo))
        git = GitCrud(repo)
        logger.info("Temporary directory: {}/.git".format(git.tmp))
        branch = self.args['--branch']
        tag = self.args['--tag']
        if branch and tag:
            logging.error("You can't define --branch and --tag, that won't work!")
            exit(1)
        if branch:
            logger.info("Checkout: {}".format(branch))
            git.checkout(branch)
        if tag:
            logger.info("Checkout: tags/{}".format(tag))
            git.checkout("tags/{}".format(tag))
        command = self.args['--command']
        if self.args['--interpreter']:
            interpreter = "{} ".format(self.args['--interpreter'])
        else:
            interpreter = ""
        if self.args['--arguements']:
            args = " {}".format(self.args['--arguements'])
        else:
            args = ""

        environment_vars = self.args['--environment']
        # set command path within local git clone
        commandpath = '{}/{}'.format(git.tmp, command)
        # formulate command
        cmd = "{interpreter}{cmd}{argv}".format(interpreter=interpreter, cmd=commandpath, argv=args)

        # export any defined environment vars
        if environment_vars:
            vars = environment_vars.split(',')
            logger.info("Exporting shell vars for sub-shell...")
            for env in vars:
                kvs = env.split('=')
                logger.info("   - export {}={}".format(kvs[0], kvs[1]))
                os.environ[kvs[0]] = kvs[1]
        try:
            logger.info("chmod 0755 {}".format(commandpath))
            os.chmod(commandpath, 0755)
        except Exception as e:
            error = "cannot chmod {}, exception: {}".format(commandpath, e)
            logger.error(error)
        logger.info("Running command: {}".format(cmd))
        (exit_code, stdout, stderr) = shell_command(cmd)
        if stdout:
            logger.info("STDOUT:")
            for line in stdout.split("\n"):
                logger.info("   {}".format(line))
        if stderr:
            logger.error("STDERR:")
            for line in stderr.split("\n"):
                logger.error("   {}".format(line))
        git.close()
        exit(exit_code)

def main():
    """Parse the CLI"""
    arguments = docopt(__doc__)

    cmd = GitExcCommand(arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
