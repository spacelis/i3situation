#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A plugin showing available space on a disk.

File: mem.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
"""
from i3situation.plugins._proc import Proc
from i3situation.plugins._utils import colored
from i3situation.plugins._plugin import Plugin

__all__ = 'NetPlugin'

KB = 1024
MB = 1024 * 1024
GB = 1024 * 1024 * 1024


def toUnit(b):
    """ convert bytes into KB or MB or GB

    :cpuinfo: @todo
    :returns: @todo

    """
    if b < KB:
        return '%6.1f B' % (b, )
    if b < MB:
        return '%6.1fKB' % (b / KB, )
    elif b < GB:
        return '%6.1fMB' % (b / MB, )


def toRxTx(s):
    """ extract rx/tx.
    :s: @todo
    :returns: @todo

    """
    nums = [int(x) for x in s.split()]
    return nums[0], nums[8]


class NetPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 1, 'menu_command': '',
                        'interfaces': ['lo']}
        self.netdev = Proc('/proc/net/dev', skip=2)
        self.prev = [toRxTx(self.netdev()[x])
                     for x in self.options['interfaces']]
        self.prev = [(x - 1, y - 1) for x, y in self.prev]
        super(NetPlugin, self).__init__(config)

    def main(self):
        """ return the formated status. """
        inv = self.options['interval']
        usage = [toRxTx(self.netdev()[x])
                 for x in self.options['interfaces']]
        d = [(y - x, v - u) for ((x, u), (y, v)) in zip(self.prev, usage)]
        full = ' '.join(['%s:⇩%s⇧%s' %
                         (k, toUnit(u[0]/inv), toUnit(u[1]/inv))
                         for k, u in zip(self.options['interfaces'], d)
                         if u[0] > 10 or u[1] > 10])
        short = ' '.join(['%s:⇩%s⇧%s' %
                         (k, toUnit(u[0]/inv), toUnit(u[1]/inv))
                         for k, u in zip(self.options['interfaces'], d)
                         if u[0] > 10 or u[1] > 10])
        #self.output_options['color'] = colored(p)
        self.prev = usage
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
