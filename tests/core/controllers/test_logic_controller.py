# -*- coding: utf-8 -*-
from unittest import TestCase

from garuda.core.controllers import GALogicController, GACoreController
from garuda.core.plugins import GALogicPlugin
from garuda.core.models import GAPluginManifest, GARequest, GAContext, GAResource


class LogicPlugin1(GALogicPlugin):

    @classmethod
    def manifest(cls):
        return GAPluginManifest(name='test.plugin1', version=1.0, identifier='test.logic.plugin1',
                                subscriptions={
                                    'fakeobject1': [GARequest.ACTION_CREATE],
                                    'shared': [GARequest.ACTION_CREATE, GARequest.ACTION_DELETE]
                                })

    def delegate(self, context):
        context.object = 'modified by LogicPlugin1'
        return context


class LogicPlugin2(GALogicPlugin):

    @classmethod
    def manifest(cls):
        return GAPluginManifest(name='test.plugin2', version=1.0, identifier='test.logic.plugin2',
                                subscriptions={
                                    'fakeobject2': [GARequest.ACTION_CREATE],
                                    'shared': [GARequest.ACTION_CREATE, GARequest.ACTION_ASSIGN]
                                })

    def delegate(self, context):
        context.object = 'modified by LogicPlugin2'
        return context


class TestLogicController(TestCase):
    """
    """

    def test_identifiers(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6}, authentication_plugins=[])
        logic_controller = GALogicController(plugins=[], core_controller=core_controller)

        self.assertEquals(logic_controller.identifier(), 'garuda.controller.logic')
        self.assertEquals(logic_controller.__class__.identifier(), 'garuda.controller.logic')

    def test_managed_plugin_type(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6}, authentication_plugins=[])
        logic_controller = GALogicController(plugins=[], core_controller=core_controller)
        self.assertEquals(logic_controller.managed_plugin_type(), GALogicPlugin)
        self.assertEquals(logic_controller.__class__.managed_plugin_type(), GALogicPlugin)

    def test_should_manage(self):
        """
        """
        plugin1 = LogicPlugin1()
        plugin2 = LogicPlugin2()

        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6}, authentication_plugins=[])
        logic_controller = GALogicController(plugins=[plugin1, plugin2], core_controller=core_controller)
        logic_controller.ready()

        managing_plugins = logic_controller._managing_plugins(resource_name='fakeobject1', action=GARequest.ACTION_CREATE)
        self.assertEquals(sorted(managing_plugins), sorted([plugin1]))

        managing_plugins = logic_controller._managing_plugins(resource_name='fakeobject1', action=GARequest.ACTION_CREATE)
        self.assertEquals(sorted(managing_plugins), sorted([plugin1]))  # do it twice to check the cache

        managing_plugins = logic_controller._managing_plugins(resource_name='fakeobject2', action=GARequest.ACTION_CREATE)
        self.assertEquals(sorted(managing_plugins), sorted([plugin2]))

        managing_plugins = logic_controller._managing_plugins(resource_name='shared', action=GARequest.ACTION_CREATE)
        self.assertEquals(sorted(managing_plugins), sorted([plugin1, plugin2]))

        managing_plugins = logic_controller._managing_plugins(resource_name='shared', action=GARequest.ACTION_DELETE)
        self.assertEquals(sorted(managing_plugins), sorted([plugin1]))

        managing_plugins = logic_controller._managing_plugins(resource_name='shared', action=GARequest.ACTION_ASSIGN)
        self.assertEquals(sorted(managing_plugins), sorted([plugin2]))

    def test_perform_delegate(self):
        """
        """
        plugin1 = LogicPlugin1()
        plugin2 = LogicPlugin2()

        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6}, authentication_plugins=[])
        logic_controller = GALogicController(plugins=[plugin1, plugin2], core_controller=core_controller)
        logic_controller.ready()

        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='fakeobject1', value=None)]

        context = GAContext(request=request, session='fake')
        context.object = 'original'

        logic_controller.perform_delegate(delegate='delegate', context=context)

        self.assertEquals(context.object, 'modified by LogicPlugin1')

        logic_controller.perform_delegate(delegate='nope', context=context)  # should not crash

    def test_perform_delegate_with_no_plugin(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6}, authentication_plugins=[])
        logic_controller = GALogicController(plugins=[], core_controller=core_controller)
        logic_controller.ready()

        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='fakeobject1', value=None)]

        context = GAContext(request=request, session='fake')
        context.object = 'original'

        logic_controller.perform_delegate(delegate='delegate', context=context)
