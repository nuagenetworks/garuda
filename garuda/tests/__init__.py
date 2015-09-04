# -*- coding: utf-8 -*-

from unittest2 import TestCase

class UnitTestCase(TestCase):
    """
    """

    def __init__(self, name):
        """
        """
        TestCase.__init__(self, name)
        self.maxDiff = None