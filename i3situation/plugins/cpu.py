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

__all__ = 'CPUPlugin'


def toSum(cpuinfo):
    """ convert cpu HZ to usage.

    :cpuinfo: @todo
    :returns: @todo

    """
    freqz = [int(x) for x in cpuinfo]
    total = sum(freqz)
    return total - freqz[3], total


class CPUPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 1, 'menu_command': ''}
        self.cpu = Proc('/proc/stat')
        self.num = len([x for x in self.cpu() if x.startswith('cpu')]) - 1
        self.prev = [toSum(self.cpu()['cpu' + str(i)])
                     for i in range(self.num)]
        self.prev = [(x - 10, y - 10) for x, y in self.prev]
        super(CPUPlugin, self).__init__(config)

    def main(self):
        """ return the formated status. """
        usage = [toSum(self.cpu()['cpu' + str(i)])
                 for i in range(self.num)]
        d = [(y - x, v - u) for ((x, u), (y, v)) in zip(self.prev, usage)]
        short = 'CPU: ' + ' '.join([percentage(u[0], u[1])[0]
                                   for u in d])
        full = 'CPU: ' + ' '.join(['%s%3d%%' % percentage(u[0], u[1])
                                   for u in d])
        #self.output_options['color'] = colored(p)
        self.prev = usage
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
