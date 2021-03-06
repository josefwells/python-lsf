"""Utility function."""

from __future__ import division

import sys
from time import strftime, localtime


def color(string, c):
    """Surround a string by shell coloring commands."""
    if not sys.stdout.isatty():
        return string
    names = {"r": 31, "g": 32, "y": 33, "b": 34}
    if c in names:
        c = names[c]
    return "\033[{}m{}\033[0m".format(c, string)


def fractioncolor(nom, denom=1):
    """Color for utilization fractions."""
    if denom == 0:
        return "r"
    fraction = nom / denom
    if fraction < .1:
        return "r"
    if fraction < .25:
        return "y"
    if fraction < .9:
        return 0
    return "g"


def format_duration(t):
    """Format a duration."""
    t = int(t)
    if t == 0:
        return "           0"
    # seconds
    s = "{:0>2}".format(t % 60)
    t //= 60
    # minutes
    if t >= 60:
        s = "{:0>2}:".format(t % 60) + s
    else:
        s = "{:>2}:".format(t % 60) + s
    t //= 60
    if t == 0:
        return "       " + s
    s = s.rjust(5, "0")
    # hours
    s = "{:>2}:".format(t % 24) + s
    t //= 24
    if t == 0:
        return "    " + s
    # days
    c = "r" if t >= 7 else "y"
    s = color("{:>2}d ".format(t), c) + s
    return s


def format_time(t):
    """Format a time stamp."""
    return strftime("%x %X", localtime(t))


def format_mem(s, c=0):
    """Format a memory size value."""
    i = 0
    while abs(s) >= 1024:
        s /= 1024
        i += 1
    e = ["B  ", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"][i]
    return color("%6.1f" % s, c) + e


def findstringpattern(strings):
    """Find a common patter in a list of string."""
    if not len(strings):
        return ""
    if all(strings[0] == s for s in strings[1:]):
        return strings[0]
    prefix = ""
    while strings[0] and all(strings[0][0] == s[0] for s in strings[1:] if s):
        prefix += strings[0][0]
        strings = [s[1:] for s in strings]
    suffix = ""
    while strings[0] and all(strings[0][-1] == s[-1]
                             for s in strings[1:] if s):
        suffix = strings[0][-1] + suffix
        strings = [s[:-1] for s in strings]
    return prefix + "*" + suffix
