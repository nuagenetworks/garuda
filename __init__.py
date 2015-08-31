# -*- coding: utf-8 -*-

import logging

# Logger
logger = logging.getLogger('Garuda')
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

from time import sleep

from bambou import BambouConfig
BambouConfig.set_should_raise_bambou_http_error(False)

from garuda.controllers import CoreController, PluginsManager
from plugins import ReaderPlugin, AnotherPlugin


def run_garuda():
    """
    """
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

    core.stop()
    logger.info('Garuda has stopped.')


if __name__ == "__main__":
    run_garuda()
