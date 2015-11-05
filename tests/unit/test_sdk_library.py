from unittest import TestCase

from garuda.core.lib import SDKLibrary

from tests.tstdk import v1_0 as tstdk1
from tests.tstdk import v1_0 as tstdk2

class TestSDKLibrary(TestCase):
    """
    """

    def test_singleton(self):
        """
        """
        lib1 = SDKLibrary()
        lib2 = SDKLibrary()
        self.assertEquals(lib1, lib2)

    def test_register_sdk(self):
        """
        """
        SDKLibrary().register_sdk('1', tstdk1)
        SDKLibrary().register_sdk('2', tstdk2)

        self.assertEquals(SDKLibrary().get_sdk('1'), tstdk1)
        self.assertEquals(SDKLibrary().get_sdk('2'), tstdk2)

    def test_unregister_sdk(self):
        """
        """
        SDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(SDKLibrary().get_sdk('1'), tstdk1)

        SDKLibrary().unregister_sdk('1')
        self.assertEquals(SDKLibrary().get_sdk('1'), None)

    def test_get_sdk_session_class(self):
        """
        """
        SDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(SDKLibrary().get_sdk_session_class('1'), tstdk1.GATSTSession)
        self.assertEquals(SDKLibrary().get_sdk_session_class('2'), None)

    def test_get_sdk_root_class(self):
        """
        """
        SDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(SDKLibrary().get_sdk_root_class('1'), tstdk1.GARoot)
        self.assertEquals(SDKLibrary().get_sdk_root_class('2'), None)

    def test_get_instance(self):
        """
        """
        SDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(SDKLibrary().get_instance('enterprise').rest_name, tstdk1.GAEnterprise.rest_name)
        self.assertEquals(SDKLibrary().get_instance('2'), None)