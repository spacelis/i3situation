#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Read proc fs.

File: _proc.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    Utility classes and functions for reading info from /proc.

"""
import re
from os.path import join as joinpath
from os.path import isfile

re.compile(r'\s+')


def parse_colon(line):
    """ Parse a line with a colon.

    :line: @todo
    :returns: @todo

    """
    k, v = line.split(':', 1)
    return k.strip(), v.strip()


def parse_vector(line, skip):
    """ Parse a line with fields separated by spaces.

    :line: @todo
    :skip: @todo
    :returns: @todo

    """
    p = line.split()
    return p[skip], p[skip + 1:]


def parse(data, lskip=0, fskip=0):
    """ strip colon and whitespace"""
    lines = data.splitlines()
    if lskip:
        lines = lines[lskip:]
    if ':' in data:
        return dict([parse_colon(l) for l in lines])
    else:
        return dict([parse_vector(l, fskip) for l in lines])


class Proc(object):

    """Docstring for Proc. """

    def __init__(self, path=None, lskip=0, fskip=0):
        """ Init """
        self._path = path or ['/', 'proc']
        if not isinstance(self._path, list):
            self._path = [self._path]
        self._lskip = lskip
        self._fskip = fskip
        self._isfile = isfile(joinpath(*self._path))
        if self._isfile:
            self._fd = open(joinpath(*self._path))
        super(Proc, self).__init__()

    def __getattr__(self, el):
        """@todo: Docstring for __getitem__.

        :arg1: @todo
        :returns: @todo

        """
        if self._isfile:
            return self()[el]
        return Proc(self._path + [el])

    def __call__(self):
        """ return updated dict
        :returns: @todo

        """
        self._fd.seek(0)
        data = self._fd.read()
        return parse(data, self._lskip, self._fskip)


def atest():
    """@todo: Docstring for function.

    :@tod: @todo
    :retrrns: @todo

    """
    import time
    print(Proc('/proc/stat')())


if __name__ == '__main__':
    atest()
