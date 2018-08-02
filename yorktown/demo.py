#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""Demo Module

Usage:
    yorktown demo --helloworld [-s STRING, -n TIMES, -b BOOL]
    yorktown demo --cmd [-c CMD]
    yorktown demo -h

Arguments:
    STRING     Change demo string output
    TIMES      Repeat string demo number of times
    BOOL       Boolean value
    CMD        A specific command to run in subprocess

Options:
    -h                          show this message
    --helloworld                run demo
    -b BOOL, --boolean BOOL     print something if boolean set
                                [default: false]
    -s STRING, --string STRING  string to show
                                [default: hello world]
    -n TIMES, --number TIMES    number of times to repeat STRING
                                [default: 1]
    -c CMD                      command to run
                                [default: ps]
"""
# protips
# yorktown demo --example [-s STRING, -n TIMES] = either option
# yorktown demo --example [-s STRING | -n TIMES] = one or the other
# changing [] to () makes optional parameters required

from docopt import docopt
from lib.utils import get_arg_option
from yorktown.lib.utils import print_arguements
from yorktown.lib.utils import AnsiColor as color
import subprocess
import sys
import os

class DemoCommand(object):
    """Demo of Modular Execution
    Argument:
        args (dict): A dictionary returned by docopt afte CLI is parsed
    """
    def __init__(self, args):
        self.args = args
        print_arguements(args)

    def helloworld(self):
        """
        hello world example
        """
        string = self.args['--string']
        count = int(self.args['--number'])
        for i in range(count):
            print(string)
        if self.args['--boolean'].lower().startswith("t"):
            print("something")

    def cmd(self):
        """
        arbitrary command example
        """
        cmd = self.args['-c']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdout, stderr) = p.communicate()
        exit_code = p.wait()
        print("EXEC:\n   {}".format(cmd))
        print("STDOUT:")
        for line in stdout.split("\n"):
            print("   {}".format(line))
        exit(exit_code)

def main():
    """Parse the CLI"""
    arguments = docopt(__doc__)

    cmd = DemoCommand(arguments)
    method = get_arg_option(arguments)
    getattr(cmd, method)()

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
