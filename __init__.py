# -*- coding: utf-8 -*-

import logging
from garuda.lib.utils import create_logger

logger = create_logger('Garuda')
logger.setLevel(logging.INFO)

from time import sleep

from bambou import BambouConfig
BambouConfig.set_should_raise_bambou_http_error(False)

from garuda.controllers import CoreController, PluginsManager
from plugins import ReaderPlugin, AnotherPlugin

# Instanciate plugins
plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)

core = CoreController()

core.start()

logger.info('Garuda is now ready.')
while True:
    try:
        sleep(3000)
    except KeyboardInterrupt:
        break

logger.info('Garuda is stopping...')
core.stop()
