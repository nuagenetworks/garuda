# -*- coding: utf-8 -*-

from garuda.controllers import CoreController, PluginsManager
from plugins import ReaderPlugin, AnotherPlugin


plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)


import signal
from time import sleep

core = CoreController()


def stop_garuda(signal, frame):
    """
    """
    core.stop()

signal.signal(signal.SIGINT, stop_garuda)

core.start()

while core.is_running():
    sleep(3)
