#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


def get_arg_option(args):
    for key, value in args.items():
        if (key != '--force' and key.startswith('--') and
                isinstance(value, bool) and value):
            return key.replace('-', '')


def print_arguements(args):
    """
    prints a pretty format version of yorktown arguements
    """
    dash = '-' * 40
    print(AnsiColor.red)
    print("{}\n              Arguements\n{}".format(dash, dash))
    print("{}{{{}".format(AnsiColor.blue, AnsiColor.yellow))
    for key, val in args.iteritems():
        print('     {:<10s}: {:<10s}'.format(key, str(val)))
    print("{}}}".format(AnsiColor.blue))
    print(AnsiColor.red)
    print("{}{}".format(dash, AnsiColor.end))


class AnsiColor(object):
    """
    life is better in color
    """
    header = '\033[95m'
    blue = '\033[1;94m'
    green = '\033[1;92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
