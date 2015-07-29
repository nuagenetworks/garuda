# -*- coding: utf-8 -*-


from controllers import ModelController, PluginsManager, CoreController
from utils import Action, GAContext, DisagreementReason, GASession, GARequest
from plugins import ReaderPlugin



plugin = ReaderPlugin()

# Register plugin
PluginsManager.register_plugin(plugin)

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

core = CoreController(session=session, request=request)
core.do_read_operation()