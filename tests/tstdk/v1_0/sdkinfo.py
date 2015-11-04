# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from gatstsession import GATSTSession
from .garoot import GARoot

class SDKInfo (object):

    @classmethod
    def api_version(cls):
        """
            Returns the api version
        """
        return 1.0

    @classmethod
    def api_prefix(cls):
        """
            Returns the api prefix
        """
        return "api"

    @classmethod
    def product_accronym(cls):
        """
            Returns the product accronym
        """
        return "TST"

    @classmethod
    def product_name(cls):
        """
            Returns the product name
        """
        return "Test"

    @classmethod
    def sdk_class_prefix(cls):
        """
            Returns the api prefix
        """
        return "GA"

    @classmethod
    def sdk_name(cls):
        """
            Returns the sdk name
        """
        return "tstdk"

    @classmethod
    def root_object_class(cls):
        """
            Returns the root object class
        """
        return GARoot

    @classmethod
    def session_class(cls):
        """
            Returns the session object class
        """
        return GATSTSession