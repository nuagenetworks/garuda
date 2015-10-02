# -*- coding: utf-8 -*-

import logging

from unittest2 import TestCase
from garuda.core import set_log_level

from vspk.vsdk.v3_2 import NURESTUser  # TODO: BAD !
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

    def get_default_user(self):
        """
        """
        return NURESTUser(id="bbbbbbbb-f93e-437d-b97e-4c945904e7bb", api_key="aaaaaaaa-98d4-4c2b-a136-770c9cbf7cdc", first_name="John", last_name="Doe")
