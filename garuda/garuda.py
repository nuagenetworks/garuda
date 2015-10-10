# -*- coding: utf-8 -*-
from time import sleep
from bambou import BambouConfig

from .core.controllers import GACoreController
from .core.plugins import GACommunicationChannel, GALogicPlugin, GAAuthenticationPlugin, GAStoragePlugin, GAPermissionsPlugin

__version__ = "1.0"

class Garuda(object):
    """
    """

    def __init__(self, sdks_info, communication_channels, plugins):
        """
        """

        BambouConfig.set_should_raise_bambou_http_error(False)

        self._sdks_info = sdks_info
        self._communication_channels = communication_channels
        self._authentication_plugins = []
        self._storage_plugins = []
        self._logic_plugins = []
        self._permission_plugins = []

        for plugin in plugins:

            if isinstance(plugin, GALogicPlugin): self._communication_channels.append(plugin)
            elif isinstance(plugin, GAAuthenticationPlugin): self._authentication_plugins.append(plugin)
            elif isinstance(plugin, GAStoragePlugin): self._storage_plugins.append(plugin)
            elif isinstance(plugin, GAPermissionsPlugin): self._permission_plugins.append(plugin)
            elif isinstance(plugin, GALogicPlugin): self._logic_plugins.append(plugin)

    def start(self):
        """
        """
        print """
                       1y9~
             .,:---,      "9"R
         ,N"`    ,jyjjRN,   `n ?            Garuda %s
       #^   y&T        `"hQ   y 'y          ==========
     (L  ;R@l                 ^a \w
    (   #^4                    Q  @
    Q  # ,W                    W  ]V        %d communications channels
   |# @L Q                    W   Q|
    V @  Vp                  ;   #^[        %d storage plugins, %d logic plugins
    ^.R[ 'Q@               ,4  .& ,T        %d permission plugins, %d authentication plugins
     (QQ  'Q4p           (R  ,BL (T
       hQ   H,`"QQQL}Q"`,;&RR   x
         "g   YQ,    ```     :F`            garuda.io
           "E,  `"B@MD&DR@B`
               '"N***xD"`

               """ % (__version__, len(self._communication_channels), len(self._storage_plugins), len(self._logic_plugins), len(self._authentication_plugins), len(self._permission_plugins))

        self.run()

    def stop(self):
        """
        """
        raise KeyboardInterrupt()

    def run(self):
        """
        """
        core = GACoreController(    sdks_info=self._sdks_info,
                                    communication_channels=self._communication_channels,
                                    logic_plugins=self._logic_plugins,
                                    authentication_plugins=self._authentication_plugins,
                                    storage_plugins=self._storage_plugins,
                                    permission_plugins=self._permission_plugins)
        core.start()

        while True:
            try:
                sleep(3000000)
            except KeyboardInterrupt:
                break

        core.stop()

