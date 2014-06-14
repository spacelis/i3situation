#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A plugin showing battery info.

File: batt.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    This plugin uses /proc/acpi/battery/BAT0 as the source.
"""
from i3situation.plugins._proc import Proc
from i3situation.plugins._utils import percentage
from i3situation.plugins._utils import colored
from i3situation.plugins._plugin import Plugin

__all__ = 'MemPlugin'


class BatteryPlugin(Plugin):

    """ A plugin for mem usage. """

    def __init__(self, config):
        self.options = {'interval': 1, 'menu_command': ''}
        self.full = Proc('/proc/acpi/battery/BAT0/info')['last full capacity']
        self.state = Proc('/proc/acpi/battery/BAT0/state')
        super(MemPlugin, self).__init__(config)

    def main(self):
        """ return the formated status. """

        short = 'BATT: %s' % (s)
        full = 'BATT: %s %s%%' % (s, p)
        #full = 'F: %(MemFree)s C: %(Cached)s B: %(Buffers)s' % self.mem()
        #full = 'F: %s C: %s B: %s' % (free // 1024,
                                      #cached // 1024,
                                      #buf // 1024)

        self.output_options['color'] = colored(p)
        return self.output(full, short)

    def on_click(self, event):
        if self.options['menu_command'] != '':
            self.display_dzen(event)
