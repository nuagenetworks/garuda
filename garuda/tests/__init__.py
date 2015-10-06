# -*- coding: utf-8 -*-

import logging

from unittest2 import TestCase
from garuda.core import set_log_level

set_log_level(logging.ERROR)

class UnitTestCase(TestCase):
    """
    """

    def __init__(self, name):
        """
        """
        super(UnitTestCase, self).__init__(name)
        self.maxDiff = None

    def set_log_level(self, level):
        """
        """
        set_log_level(level)
