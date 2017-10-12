#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
from past.builtins import basestring
import sys

import termcolor


def colored(text, color):
    return termcolor.colored(text, color) if sys.stdout.isatty() else text


def print_result(extractor):
    if extractor.failures_number:
        print_errors(extractor)
    else:
        print_success(extractor)


def print_success(extractor):
    print()
    print(colored('✓ %s' % extractor.description, 'green'))
    print()


def print_errors(extractor):
    print()
    print(colored(extractor.description, 'yellow'))
    print()

    print(format_errors(extractor.get_failures()))
    print()


def format_errors(errors):
    ret = []
    for error in errors:
        ret.extend(_print(error, [], 0))
    return '\n'.join(ret)


def _print(obj, buffer, level):
    for title, desc in obj.items():
        buffer.append((level * 2 * ' ') + title)
        if desc and isinstance(desc[0], basestring):
            for err in desc:
                buffer.append(colored('%s  ✗ %s' % ((level * 2 * ' '), err), 'red'))
        else:
            level += 1
            for suite in desc:
                _print(suite, buffer, level)

    return buffer

