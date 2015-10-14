# -*- coding: utf-8 -*-
import os, sys
import signal
import logging

from garuda.core.controllers import GACoreController
from garuda.core.channels import GAChannel
from garuda.core.lib import ThreadManager

logger = logging.getLogger('garuda.controller.channels')

class GAChannelsController(object):
    """

    """
    def __init__(self, channels, redis_info, logic_plugins, authentication_plugins, storage_plugins, permission_plugins):
        """
        """
        self._channels = channels
        self._redis_info = redis_info
        self._logic_plugins = logic_plugins
        self._authentication_plugins = authentication_plugins
        self._storage_plugins = storage_plugins
        self._permission_plugins = permission_plugins

        self._channel_pids = []

    # Implementation

    def start(self):
        """
        """
        logger.info("Forking communication channels...")

        for channel in self._channels:

            pid = os.fork()
            if not pid:
                break
            else:
                self._channel_pids.append(pid)
                logger.info('Channel %s forked with pid: %s' % (channel.manifest().identifier, pid))

        if not pid:
            core = GACoreController(redis_info=self._redis_info, logic_plugins=self._logic_plugins,
                                    authentication_plugins=self._authentication_plugins, storage_plugins=self._storage_plugins,
                                    permission_plugins=self._permission_plugins)

            channel.run(core_controller=core)
            logger.info("Channels subprocess %s exited gracefuly." % os.getpid())
            sys.exit(0)
        else:
            logger.info("All channels successfully forked")

    def stop(self):
        """
        """
        for pid in self._channel_pids:
            logger.info("Killing channels with pid %s" % pid)
            os.kill(pid, signal.SIGTERM)
