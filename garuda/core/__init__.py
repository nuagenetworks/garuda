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

from garuda.core.controllers import CoreController, PluginsManager
from garuda.plugins import ReaderPlugin, AnotherPlugin
from garuda.plugins import DefaultAuthenticationPlugin, DefaultModelControllerPlugin


def main():
    """
    """
    # Instanciate plugins
    plugin = ReaderPlugin()
    anotherplugin = AnotherPlugin()
    default_model_controller = DefaultModelControllerPlugin()
    default_authentication_plugin = DefaultAuthenticationPlugin()

    # Register plugin
    # PluginsManager.register_plugin(plugin)
    # PluginsManager.register_plugin(anotherplugin)

    core = CoreController(authentication_plugins=[default_authentication_plugin], model_controller_plugins=[default_model_controller])
    core.start()

    logger.info('Garuda is now ready. (Press CTRL+C to quit)')
    while True:
        try:
            sleep(3000)
        except KeyboardInterrupt:
            break

    core.stop()
    logger.info('Garuda has stopped.')


if __name__ == "__main__":
    main()
