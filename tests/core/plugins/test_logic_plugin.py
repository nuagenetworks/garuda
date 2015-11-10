from unittest import TestCase

from garuda.core.plugins import GALogicPlugin
from garuda.core.models import GAPluginManifest, GARequest


class FakeLogicPlugin(GALogicPlugin):

    @classmethod
    def manifest(cls):
        return GAPluginManifest(name='test.plugin', version=1.0, identifier="test.logic.plugin",
                                subscriptions={
                                    "fakeobject1": [GARequest.ACTION_UPDATE, GARequest.ACTION_DELETE],
                                    "fakeobject2": [GARequest.ACTION_CREATE, GARequest.ACTION_READ],
                                    "fakeobject3": [GARequest.ACTION_DELETE, GARequest.ACTION_READALL],
                                    "fakeobject4": [GARequest.ACTION_ASSIGN]
                                })


class TestLogicPlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GALogicPlugin()

        self.assertTrue(plugin.will_perform_read(context=True))
        self.assertTrue(plugin.did_perform_read(context=True))

        self.assertTrue(plugin.will_perform_readall(context=True))
        self.assertTrue(plugin.did_perform_readall(context=True))

        self.assertTrue(plugin.will_perform_create(context=True))
        self.assertTrue(plugin.did_perform_create(context=True))

        self.assertTrue(plugin.will_perform_update(context=True))
        self.assertTrue(plugin.did_perform_update(context=True))

        self.assertTrue(plugin.will_perform_delete(context=True))
        self.assertTrue(plugin.did_perform_delete(context=True))

        self.assertTrue(plugin.will_perform_assign(context=True))
        self.assertTrue(plugin.did_perform_assign(context=True))

    def test_should_manage(self):
        """
        """
        plugin = FakeLogicPlugin()

        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_CREATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_UPDATE), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_READ), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_READALL), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_DELETE), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject1', action=GARequest.ACTION_ASSIGN), False)

        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_CREATE), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_UPDATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_READ), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_READALL), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_DELETE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject2', action=GARequest.ACTION_ASSIGN), False)

        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_CREATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_UPDATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_READ), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_READALL), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_DELETE), True)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject3', action=GARequest.ACTION_ASSIGN), False)

        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_CREATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_UPDATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_READ), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_READALL), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_DELETE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject4', action=GARequest.ACTION_ASSIGN), True)

        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_CREATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_UPDATE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_READ), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_READALL), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_DELETE), False)
        self.assertEquals(plugin.should_manage(rest_name='fakeobject5', action=GARequest.ACTION_ASSIGN), False)
