#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A plugin showing available memory.

File: io.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    This plugin collects usage of net and local I/O.
    Only the interface of top usage is shown.
"""
from i3situation.plugins._proc import Proc
from i3situation.plugins._utils import colored
from i3situation.plugins._plugin import Plugin

__all__ = 'IOPlugin'

KB = 1024
MB = 1024 * 1024
GB = 1024 * 1024 * 1024


def withUnit(b):
    """ convert bytes into KB or MB or GB

    :b: number of bytes
    :returns: human friendly string

    """
    if b < KB:
        return '%6.1f B' % (b, )
    if b < MB:
        return '%6.1fKB' % (b / KB, )
    elif b < GB:
        return '%6.1fMB' % (b / MB, )


def fromNetInt(s):
    """ extract rx/tx.
    :s: @todo
    :returns: (recieved, transmit)

    """
    s = s.split()
    return int(s[0]), int(s[8])


def fromDisk(s):
    """ extract RW stats

    :s: @todo
    :returns: @todo

    """
    return int(s[4]) * 512, int(s[0]) * 512


class IOPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 1, 'menu_command': '',
                        'interfaces': None, 'disks': None}
        self.netdev = Proc('/proc/net/dev', lskip=2)
        self.diskdev = Proc('/proc/diskstats', fskip=2)
        self.interfaces = (self.options['interfaces'] or
                           list(self.netdev().keys()))
        self.partitions = self.options['disks'] or list(self.diskdev().keys())
        self.prev = self.get_usage()
        self.prev = [(x - 1, y - 1) for x, y in self.prev]
        super(IOPlugin, self).__init__(config)

    def get_usage(self):
        """ return the usage directory.

        :netint: @todo
        :disks: @todo
        :returns: @todo

        """
        return ([fromNetInt(self.netdev()[x])
                 for x in (self.interfaces)] +
                [fromDisk(self.diskdev()[x])
                 for x in (self.partitions)])

    def main(self):
        """ return the formated status. """
        inv = self.options['interval']
        usage = self.get_usage()
        d = [(y - x, v - u) for (x, u), (y, v) in zip(self.prev, usage)]
        sd = sorted(zip(self.interfaces + self.partitions, d),
                    key=lambda x: x[1][0] + x[1][1],
                    reverse=True)
        top = sd[0]
        full = '%5s: ▼%s ▲%s' % (
            top[0],
            withUnit(top[1][0]/inv),
            withUnit(top[1][1]/inv))
        short = full
        #self.output_options['color'] = colored(p)
        self.prev = usage
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
