# -*- coding: utf-8 -*-

from .abstracts import GAPlugin


class GAAuthenticationPlugin(GAPlugin):
    """
    """

    def should_manage(self, request):
        """
        """
        return True

    def authenticate(self, request):
        """
        """
        raise NotImplementedError("%s should implement authenticate method" % self)