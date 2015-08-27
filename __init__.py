# -*- coding: utf-8 -*-

from bambou import BambouConfig
BambouConfig.set_should_raise_bambou_http_error(False)


from garuda.controllers import CoreController, PluginsManager
from plugins import ReaderPlugin, AnotherPlugin


plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)


from time import sleep

core = CoreController()

core.start()

print 'Garuda is now ready.'
while True:
    try:
        sleep(3000)
    except KeyboardInterrupt:
        break

print 'Garuda is stopping...'
core.stop()