# -*- coding: utf-8 -*-

from .plugin import GAPlugin


class GAAuthenticationPlugin(GAPlugin):
    """
    """

    def should_manage(self, request):
        """
        """
        return True

    def extract_session_identifier(self, request):
        ""
        ""
        return

    def authenticate(self, request):
        """
        """
        raise NotImplementedError("%s should implement authenticate method" % self)