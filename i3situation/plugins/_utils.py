#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Utility function.

File: _utils.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:


"""
from bisect import bisect

DEFUALT_PALLETE = {'colors': ['#ff4400', '#ffff00', '#aaff00', '#00ff00'],
                   'limits': [10, 30, 50]}


def percentage(v, t):
    """ return a symbol reflecting the percentages. """
    p = (v * 800 + 4) // t // 8
    e = (v * 64 + 4) // t // 8
    eigths = '▁▂▃▄▅▆▇██'
    return eigths[e], p


def colored(p, pallete=None, inverse=False):
    """ return a color code for the percentage. """
    pallete = pallete or DEFUALT_PALLETE
    if inverse:
        return pallete['colors'][len(pallete['colors']) -
                                 bisect(pallete['limits'], p)]
    return pallete['colors'][bisect(pallete['limits'], p)]
