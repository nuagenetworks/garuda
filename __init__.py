# -*- coding: utf-8 -*-


from controllers import ModelController, PluginsManager, OperationsManager, CoreController
from utils import GAContext, DisagreementReason, GASession, GARequest, Resource
from plugins import ReaderPlugin, AnotherPlugin



plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)


from channels import RESTCommunicationChannel
from time import sleep

cc = RESTCommunicationChannel()

def stop_flask(signal, frame):
    'CTRL+C captured'
    cc.stop()

import signal
signal.signal(signal.SIGINT, stop_flask)

cc.start()

while not cc.thread.stopped():
    print 'Flask is alive !'
    sleep(5)