# -*- coding: utf-8 -*-
import logging
from time import sleep
from bambou import BambouConfig

logger = logging.getLogger('garuda')

from .core.controllers import GACoreController
from .core.channels import GAChannel
from .core.plugins import GALogicPlugin, GAAuthenticationPlugin, GAStoragePlugin, GAPermissionsPlugin

__version__ = '1.0'



class Garuda(object):
    """
    """

    def __init__(self, sdks_info, redis_info=None, channels=[], plugins=[], log_level=logging.INFO, log_handler=None, runloop=True, banner=True, debug=True):
        """
        """

        BambouConfig.set_should_raise_bambou_http_error(False)

        self._redis_info = redis_info if redis_info else {'host': '127.0.0.1', 'port': '6379', 'db': 0}
        self._runloop = runloop
        self._sdks_info = sdks_info
        self._channels = channels
        self._authentication_plugins = []
        self._storage_plugins = []
        self._logic_plugins = []
        self._permission_plugins = []
        self._debug = debug

        for plugin in plugins:

            if isinstance(plugin, GALogicPlugin): self._channels.append(plugin)
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

        self.core = GACoreController(   sdks_info=self._sdks_info,
                                        redis_info=self._redis_info,
                                        channels=self._channels,
                                        logic_plugins=self._logic_plugins,
                                        authentication_plugins=self._authentication_plugins,
                                        storage_plugins=self._storage_plugins,
                                        permission_plugins=self._permission_plugins)


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
     (L  ;R@l                 ^a \w       github.com/nuagenetworks/garuda
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

               """ % (__version__,
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
            try:
                import pdb, objgraph, resource, guppy
                print '# DEBUGGING MODE: Debugging mode active'
                print '# DEBUGGING MODE: Collecting initial heap snaphot...'
                hp = guppy.hpy()
                heap_initial = hp.heap()
                print '# DEBUGGING MODE: Initial heap snaphot collected'
                print '# DEBUGGING MODE: Hit CTRL-C to enter the debugging mode at anytime'
            except:
                print '# DEBUGGING MODE: Cannot use debugging mode. Modules needed: `pdb`, `resource`, `objgraph` and `guppy`'
                self._debug = False
            finally:
                print ''

        self.core.start()

        if self._runloop:
            while True:
                try:
                    sleep(300000)
                except KeyboardInterrupt:
                    break

        if self._debug:
            import pdb, objgraph, resource, guppy
            print ''
            print '# DEBUGGING MODE: Entering debugging mode...'
            print '# DEBUGGING MODE: Final Memory Usage : %f (MB)' % (float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024 / 1024)
            print '# DEBUGGING MODE: Collecting final heap snaphot...'
            hp = guppy.hpy()
            heap_final = hp.heap()
            print '# DEBUGGING MODE: Final heap snaphot collected'
            print '# DEBUGGING MODE: You can see the heap snaphots in variables `heap_initial` and `heap_final`'
            print '# DEBUGGING MODE: Starting pdb. Type `c` to terminate Garuda.'
            print ''
            pdb.set_trace()

        self.core.stop()

    def stop(self):
        """
        """
        self.core.stop()

