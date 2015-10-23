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
        ""
        ""
        return

    def authenticate(self, request):
        """
        """
        raise NotImplementedErrorError("%s should implement authenticate method" % self)