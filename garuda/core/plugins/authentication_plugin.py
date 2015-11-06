# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin


class GAAuthenticationPlugin(GAPlugin):
    """
    """

    def should_manage(self, request):  # pragma: no cover
        """
        """
        return True

    def extract_session_identifier(self, request):  # pragma: no cover
        ""
        ""
        return

    def authenticate(self, request):  # pragma: no cover
        """
        """
        raise NotImplementedError("%s should implement authenticate method" % self)
