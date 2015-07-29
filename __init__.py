# -*- coding: utf-8 -*-


from controllers import ModelController, PluginsManager, OperationsManager, CoreController
from utils import GAContext, DisagreementReason, GASession, GARequest
from plugins import ReaderPlugin, AnotherPlugin



plugin = ReaderPlugin()
anotherplugin = AnotherPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)
PluginsManager.register_plugin(anotherplugin)

class Resource(object):

    def __init__(self):
        """
        TMP
        """
        self.rest_name = 'subnet'


request = GARequest(method='GET', url='/toto')

session = GASession()
session.resource = Resource()
session.user = 'me'
session.data = {}
session.action = 'create'

# Orechestrator
core = CoreController(session=session, request=request)

# Will be a separated worker later, launched by the core controller
operation = OperationsManager(context=core.context)
operation.do_read_operation()