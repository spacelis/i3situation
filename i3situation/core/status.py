import sys
from collections import OrderedDict
import logging
import time
import json
import os
from i3situation.core import pluginManager
from i3situation.core import config


class Status():
    """
    Handles the running of the status utility and acts as the glue for the
    application.
    """
    def __init__(self):
        self.config = config.Config()
        self.outputDict = OrderedDict()
        self._configFilePath = self.config.configPath
        self._pluginPath = self.config.pluginPath
        self._configModTime = os.path.getmtime(self._configFilePath)
        self._pluginModTime = os.path.getmtime(self._pluginPath)
        logger = logging.getLogger()
        # If a stream handler has been attached, remove it.
        if logger.handlers:
            logger.removeHandler(logger.handlers[0])
        handler = logging.FileHandler(self.config.generalSettings['logFile'])
        logger.addHandler(handler)
        formatter = logging.Formatter(('[%(asctime)s] - %(levelname)s'
           ' - %(filename)s - %(funcName)s - %(message)s'),
           '%d/%m/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        logger.setLevel(self.config.generalSettings['loggingLevel'])
        handler.setLevel(self.config.generalSettings['loggingLevel'])
        logging.debug('Config loaded from {0}'.format(self._configFilePath))
        logging.debug('Plugin path is located at {0}'.format(self._pluginPath))
        logging.debug('Last config modification time is: {0}'.format(self._configModTime))
        logging.debug('Last plugin directory modification time is: {0}'.format(self._pluginModTime))
        self.outputToBar('{\"version\":1}', False)
        self.outputToBar('[', False)
        logging.debug('Sent initial JSON data to i3bar.')
        logging.debug('Beginning plugin loading process')
        self.loader = pluginManager.PluginLoader(
            self._pluginPath, self.config.pluginSettings)
        self.threadManager = pluginManager.ThreadManager(self.outputDict)

    def outputToBar(self, message, comma=True):
        """
        Outputs data to stdout, without buffering.
        """
        if comma:
            message += ','
        sys.stdout.write(message + '\n')
        sys.stdout.flush()

    def reload(self):
        """
        Reload the installed plugins and the configuration file. This is called
        when either the plugins or config get updated.
        """
        logging.debug('Reloading config file as files have been modified.')
        self.config.pluginSettings, self.config.generalSettings = self.config.reload()
        logging.debug('Reloading plugins as files have been modified.')
        self.loader = pluginManager.PluginLoader(
            self._pluginPath, self.config.pluginSettings)
        self._pluginModTime = os.path.getmtime(self._pluginPath)
        self._configModTime = os.path.getmtime(self._configFilePath)

    def runPlugins(self):
        """
        Creates a thread for each plugin and lets the ThreadManager handle it.
        """
        for obj in self.loader.objects:
            # Reserve a slot in the outputDict in order to ensure that the
            # items are in the correct order.
            self.outputDict[obj._outputOptions['name']] = None
            self.threadManager.addThread(obj.main, obj.options['interval'])

    def run(self):
        """
        Monitors if the config file or plugins are updated. Also outputs the
        JSON data generated by the plugins, without needing to poll the threads.
        """
        self.runPlugins()
        while True:
            # Reload plugins and config if either the config file or plugin
            # directory are modified.
            if self._configModTime != os.path.getmtime(self._configFilePath) or \
            self._pluginModTime != os.path.getmtime(self._pluginPath):
                self.threadManager.killAllThreads()
                self.reload()
                self.runPlugins()
            self.outputToBar(json.dumps(list(self.outputDict.values())))
            logging.debug('Output to bar')
            time.sleep(self.config.generalSettings['interval'])
