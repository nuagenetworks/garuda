# -*- coding: utf-8 -*-


from controllers import ModelController, PluginsManager, OperationsManager, CoreController
from utils import GAContext, DisagreementReason, GASession, GARequest, Resource
from plugins import ReaderPlugin, AnotherPlugin



plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)


from controllers import CoreController
import signal
from time import sleep

core = CoreController()

def stop_garuda(signal, frame):
    core.stop()

signal.signal(signal.SIGINT, stop_garuda)

core.start()

while core.is_running():
    sleep(2)

print 'The End'
