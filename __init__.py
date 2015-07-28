# -*- coding: utf-8 -*-


from controllers import ModelController, PluginController, CoreController
from utils import Action, GAContext, DisagreementReason
from plugins import MyPlugin



plugin = MyPlugin()

# Adding callback
PluginController.register_callback(Action.PRE_CREATE, plugin.precreate_callback)
PluginController.register_callback(Action.PRE_CREATE, plugin.precreate_callback2)
PluginController.register_callback(Action.POST_CREATE, plugin.postcreate_callback)

core = CoreController(session='mysession', request='myrequest')
core.do_the_job()