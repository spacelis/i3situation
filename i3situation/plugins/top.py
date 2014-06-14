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
from os import listdir
from os.path import join as pjoin
from collections import Counter
import re
from i3situation.plugins._utils import colored
from i3situation.plugins._plugin import Plugin

__all__ = 'TopPlugin'

PID = re.compile(r'\d+')


def top(prev=None):
    """ return the commanline of the top running process. """
    pcs = [p for p in listdir('/proc/') if PID.match(p)]
    utimes = Counter()
    for p in pcs:
        try:
            with open(pjoin('/proc', p, 'stat')) as f:
                s = f.read().strip().split()
                utimes['%s %s' % (p, s[1])] = int(s[13])
        except FileNotFoundError:
            pass
    if not prev:
        top_pc, _ = utimes.most_common(1)[0]
    else:
        top_pc, _ = (utimes - prev).most_common(1)[0]
    #with open(pjoin('/proc', top_pc[0], 'cmdline')) as f:
        #top_cmd = f.read()
    pid, cmd = top_pc.split()

    return int(pid), cmd[1:-1], utimes


class TopPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 5, 'menu_command': ''}
        self.prev = None
        super(TopPlugin, self).__init__(config)

    def main(self):
        """ return the formated status. """
        pid, cmd, self.prev = top(self.prev)
        full = 'TOP: %6d %8s' % (pid, cmd[:8])
        short = 'TOP: %6d %3s' % (pid, cmd[:3])
        #self.output_options['color'] = colored(p)
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
