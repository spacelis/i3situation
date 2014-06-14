#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A plugin showing available memory.

File: mem.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    This plugin uses /proc/meminfo as the source.
    The free% = (MemFree + Cached + Buffers) / MemTotal * 100
"""
from i3situation.plugins._proc import Proc
from i3situation.plugins._utils import percentage
from i3situation.plugins._utils import colored
from i3situation.plugins._plugin import Plugin

__all__ = 'MemPlugin'


def toKBytes(s):
    """ Convert to int """
    return int(s[:-3])


class MemPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 1, 'menu_command': ''}
        self.mem = Proc('/proc/meminfo')
        self.tot = toKBytes(self.mem.MemTotal)
        super(MemPlugin, self).__init__(config)

    def main(self):
        """ return the formated status. """
        free = toKBytes(self.mem.MemFree)
        cached = toKBytes(self.mem.Cached)
        buf = toKBytes(self.mem.Buffers)
        s, p = percentage(free + cached + buf, self.tot)

        short = 'Mem: %s' % (s)
        full = 'Mem: %s %s%%' % (s, p)
        #full = 'F: %(MemFree)s C: %(Cached)s B: %(Buffers)s' % self.mem()
        #full = 'F: %s C: %s B: %s' % (free // 1024,
                                      #cached // 1024,
                                      #buf // 1024)

        self.output_options['color'] = colored(p)
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
