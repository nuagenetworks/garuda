from unittest import TestCase

from garuda.core.controllers import GACoreController
from garuda.core.models import GAPluginManifest, GARequest, GAPlugin, GAPluginController

class FakePlugin1(GAPlugin):

    @classmethod
    def manifest(cls):
        return GAPluginManifest(name='fake.plugin1', version=1.0, identifier="fake.plugin1")


class FakePlugin2(GAPlugin):

    @classmethod
    def manifest(cls):
        return GAPluginManifest(name='fake.plugin2', version=1.0, identifier="fake.plugin2")


class FakePluginController(GAPluginController):

    @classmethod
    def managed_plugin_type(cls):
        return FakePlugin1

class TestPluginPlugin(TestCase):
    """
    """

    def test_managed_plugin_type(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[])
        self.assertEquals(controller.managed_plugin_type(), FakePlugin1)
        self.assertEquals(controller.__class__.managed_plugin_type(), FakePlugin1)

        abstract = GAPluginController(core_controller=core_controller, plugins=[])

        with self.assertRaises(NotImplementedError):
            abstract.managed_plugin_type()

        with self.assertRaises(NotImplementedError):
            abstract.__class__.managed_plugin_type()

    def test_valid_plugin_resistration(self):
        """
        """
        plugin = FakePlugin1()

        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[])
        controller.register_plugin(plugin)

        self.assertEquals(len(controller.plugins), 1)
        self.assertEquals(controller.plugins[0], plugin)

        with self.assertRaises(AssertionError):
            controller.register_plugin(plugin)


    def test_invalid_plugin_resistration(self):
        """
        """
        plugin = FakePlugin2()
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[plugin])

        with self.assertRaises(AssertionError):
            controller.register_plugin(plugin)

    def test_ready_auto_registration(self):
        """
        """
        plugin = FakePlugin1()

        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[plugin])
        controller.ready()

        self.assertEquals(len(controller.plugins), 1)
        self.assertEquals(controller.plugins[0], plugin)


    def test_unregister_plugin(self):
        """
        """
        plugin = FakePlugin1()

        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[])
        controller.register_plugin(plugin)

        self.assertEquals(len(controller.plugins), 1)
        self.assertEquals(controller.plugins[0], plugin)

        controller.unregister_plugin(plugin)
        self.assertEquals(len(controller.plugins), 0)

        with self.assertRaises(AssertionError):
            controller.unregister_plugin(plugin)

    def test_unregister_all_plugins(self):
        """
        """
        plugin1 = FakePlugin1()
        plugin2 = FakePlugin1()

        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        controller = FakePluginController(core_controller=core_controller, plugins=[plugin1, plugin2])
        controller.ready()

        self.assertEquals(len(controller.plugins), 2)
        self.assertEquals(controller.plugins[0], plugin1)
        self.assertEquals(controller.plugins[1], plugin2)

        controller.unregister_all_plugins()

        self.assertEquals(len(controller.plugins), 0)
