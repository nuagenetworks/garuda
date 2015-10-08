# -*- coding: utf-8 -*-

import importlib
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

from garuda.core.controllers import GACoreController, GABusinessLogicPluginsManager

def set_log_level(level):
    """
    """
    logger.setLevel(level)


def main():
    """
    """
    from garuda.plugins import DefaultAuthenticationPlugin, DefaultGAModelControllerPlugin, DefaultGAPermissionsControllerPlugin
    from garuda.core.lib import SDKsManager
    from garuda.channels.rest import RESTCommunicationChannel

    rest_comm_channel = RESTCommunicationChannel(host="0.0.0.0", port=2000, threaded=True, debug=True, use_reloader=False)


    sdks_manager = SDKsManager()
    sdks_manager.register_sdk(identifier="vspk32", sdk=importlib.import_module('vspk.v3_2'))

    # Instanciate plugins
    default_model_controller = DefaultGAModelControllerPlugin()
    default_authentication_plugin = DefaultAuthenticationPlugin()
    default_permission_controller_plugin = DefaultGAPermissionsControllerPlugin()

    core = GACoreController(  sdks_manager=sdks_manager,
                            communication_channels=[rest_comm_channel],
                            authentication_plugins=[default_authentication_plugin],
                            model_controller_plugins=[default_model_controller],
                            permission_controller_plugins=[default_permission_controller_plugin])
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
