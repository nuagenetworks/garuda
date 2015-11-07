from unittest import TestCase

from garuda.core.lib import GASDKLibrary

from tests.tstdk import v1_0 as tstdk1
from tests.tstdk import v1_0 as tstdk2


class TestSDKLibrary(TestCase):
    """
    """

    def test_singleton(self):
        """
        """
        lib1 = GASDKLibrary()
        lib2 = GASDKLibrary()
        self.assertEquals(lib1, lib2)

    def test_register_sdk(self):
        """
        """
        GASDKLibrary().register_sdk('1', tstdk1)
        GASDKLibrary().register_sdk('2', tstdk2)

        self.assertEquals(GASDKLibrary().get_sdk('1'), tstdk1)
        self.assertEquals(GASDKLibrary().get_sdk('2'), tstdk2)

        GASDKLibrary().unregister_sdk('1')
        GASDKLibrary().unregister_sdk('2')

        with self.assertRaises(IndexError):
            GASDKLibrary().get_sdk('1')

        with self.assertRaises(IndexError):
            GASDKLibrary().get_sdk('2')

    def test_get_sdk_session_class(self):
        """
        """
        GASDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(GASDKLibrary().get_sdk_session_class('1'), tstdk1.GATSTSession)

        with self.assertRaises(IndexError):
            GASDKLibrary().get_sdk_session_class('2')

        GASDKLibrary().unregister_sdk('1')

    def test_get_sdk_root_class(self):
        """
        """
        GASDKLibrary().register_sdk('1', tstdk1)
        self.assertEquals(GASDKLibrary().get_sdk_root_class('1'), tstdk1.GARoot)

        with self.assertRaises(IndexError):
            GASDKLibrary().get_sdk_root_class('2')

        GASDKLibrary().unregister_sdk('1')
