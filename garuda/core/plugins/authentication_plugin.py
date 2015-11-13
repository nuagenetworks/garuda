# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin


class GAAuthenticationPlugin(GAPlugin):
    """
    """

    def should_manage(self, request):
        """
        """
        return True

    def extract_session_identifier(self, request):
        """
        """
        raise NotImplementedError("%s must implement extract_session_identifier method" % self)

    def authenticate(self, request):
        """
        """
        raise NotImplementedError("%s must implement authenticate method" % self)
