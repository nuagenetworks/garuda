# -*- coding: utf-8 -*-

import logging

from unittest import TestCase

class UnitTestCase(TestCase):
    """
    """

    def __init__(self, name):
        """
        """
        super(UnitTestCase, self).__init__(name)
        self.maxDiff = None
