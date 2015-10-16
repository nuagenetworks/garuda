# -*- coding: utf-8 -*-
import logging
import os
import importlib
from time import sleep
from bambou import BambouConfig
from setproctitle import setproctitle

logger = logging.getLogger('garuda')

from .core.lib import SDKLibrary
from .core.controllers import GACoreController, GAChannelsController
from .core.channels import GAChannel
from .core.plugins import GALogicPlugin, GAAuthenticationPlugin, GAStoragePlugin, GAPermissionsPlugin

__version__ = '1.0'


class Garuda(object):
    """
    """

    def __init__(self, sdks_info, redis_info=None, channels=[], plugins=[], log_level=logging.INFO, log_handler=None, runloop=True, banner=True, debug=False):
        """
        """
        setproctitle('garuda-server')
        BambouConfig.set_should_raise_bambou_http_error(False)

        self._redis_info = redis_info if redis_info else {'host': '127.0.0.1', 'port': '6379', 'db': 0}
        self._runloop = runloop
        self._sdks_info= sdks_info
        self._sdk_library = SDKLibrary()
        self._channels = channels
        self._authentication_plugins = []
        self._storage_plugins = []
        self._logic_plugins = []
        self._permission_plugins = []
        self._debug = debug


        for sdk_info in self._sdks_info:
            self._sdk_library.register_sdk(identifier=sdk_info['identifier'], sdk=importlib.import_module(sdk_info['module']))

        for plugin in plugins:

            if isinstance(plugin, GAChannel): self._channels.append(plugin)
            elif isinstance(plugin, GAAuthenticationPlugin): self._authentication_plugins.append(plugin)
            elif isinstance(plugin, GAStoragePlugin): self._storage_plugins.append(plugin)
            elif isinstance(plugin, GAPermissionsPlugin): self._permission_plugins.append(plugin)
            elif isinstance(plugin, GALogicPlugin): self._logic_plugins.append(plugin)

        if banner:
            self.print_banner()

        if not log_handler:
            log_handler = logging.StreamHandler()
            log_handler.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: %(message)s'))
            logger.addHandler(log_handler)

        logger.setLevel(log_level)

        self._channels_controller = GAChannelsController(channels=self._channels,
                                                         redis_info=self._redis_info,
                                                         logic_plugins=self._logic_plugins,
                                                         authentication_plugins=self._authentication_plugins,
                                                         storage_plugins=self._storage_plugins,
                                                         permission_plugins=self._permission_plugins)


    def _init_debug_mode(self):
        """
        """
        try:
            import ipdb, objgraph, resource, guppy, signal
            print '# DBG MODE: Debug Mode active'
            print '# DBG MODE: Initial memory usage : %f (MB)' % (float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024 / 1024)
            print '# DBG MODE: Collecting initial heap snaphot...'
            hp = guppy.hpy()
            heap_initial = hp.heap()

            def handle_signal(signal_number, frame_stack):
                self._launch_debug_mode()

            signal.signal(signal.SIGHUP, handle_signal)

            print '# DBG MODE: Initial heap snaphot collected'
            print '# DBG MODE: Do a `kill -HUP %s` to enter the debug mode at anytime' % os.getpid()
            print '# DBG MODE: Hitting CTRL+C stop Garuda then enter the debugg mode.'
        except:
            print '# DBG MODE: Cannot use Debugging Mode. Modules needed: `ipdb`, `resource`, `objgraph` and `guppy`'
            self._debug = False
        finally:
            print ''

    def _launch_debug_mode(self):
        """
        """
        import ipdb, objgraph, resource, guppy
        print ''
        print '# DBG MODE: Entering Debugging Mode...'
        print '# DBG MODE: Final memory usage : %f (MB)' % (float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024 / 1024)
        print '# DBG MODE: Collecting final heap snaphot...'
        hp = guppy.hpy()
        heap_current = hp.heap()
        print '# DBG MODE: Current heap snaphot collected'
        print '# DBG MODE: You can see the heap snaphots in variables `heap_initial` and `heap_current`'
        print '# DBG MODE: Starting ipdb (CTRL+D to exit)'
        print ''
        ipdb.set_trace()


    def print_banner(self):
        """
        """
        all_sdks = ', '.join([item['module'] for item in self._sdks_info])
        all_channels = ', '.join([channel.manifest().name for channel in self._channels])
        all_storages = ', '.join([plugin.manifest().name for plugin in self._storage_plugins])
        all_auth = ', '.join([plugin.manifest().name for plugin in self._authentication_plugins])
        all_perms = ', '.join([plugin.manifest().name for plugin in self._permission_plugins])

        print """
                       1y9~
             .,:---,      "9"R            Garuda %s
         ,N"`    ,jyjjRN,   `n ?          ==========
       #^   y&T        `"hQ   y 'y
     (L  ;R@l                 ^a \w       PID: %d
    (   #^4                    Q  @
    Q  # ,W                    W  ]V      %d channel%s           %s
   |# @L Q                    W   Q|      %s sdk%s               %s
    V @  Vp                  ;   #^[      %d storage plugin%s    %s
    ^.R[ 'Q@               ,4  .& ,T      %d auth plugin%s       %s
     (QQ  'Q4p           (R  ,BL (T       %d permission plugin%s %s
       hQ   H,`"QQQL}Q"`,;&RR   x
         "g   YQ,    ```     :F`          %d logic plugin%s
           "E,  `"B@MD&DR@B`
               '"N***xD"`

               """ % (__version__, os.getpid(),
                       len(self._channels), "s" if len(self._channels) > 1 else "", ": %s" % all_channels if len(all_channels) else "",
                       len(self._sdks_info), "s" if len(self._sdks_info) > 1 else "", ": %s" % all_sdks if len(all_sdks) else "",
                       len(self._storage_plugins), "s" if len(self._storage_plugins) > 1 else "", ": %s" % all_storages if len(all_storages) else "",
                       len(self._authentication_plugins), "s" if len(self._authentication_plugins) > 1 else "", ": %s" % all_auth if len(all_auth) else "",
                       len(self._permission_plugins), "s" if len(self._permission_plugins) > 1 else "", ": %s" % all_perms if len(all_perms) else "",
                       len(self._logic_plugins), "s" if len(self._logic_plugins) > 1 else "")

    def start(self):
        """
        """
        if self._debug:
            self._init_debug_mode()

        self._channels_controller.start()
        logger.info('Garuda is up and ready to rock! (press CTRL-C to exit)')

        if self._runloop:
            while True:
                try:
                    sleep(300000)
                except KeyboardInterrupt:
                    break

        self.stop()

    def stop(self):
        """
        """
        self._channels_controller.stop()

        logger.info('Garuda is stopped')

        if self._debug:
            self._launch_debug_mode()
