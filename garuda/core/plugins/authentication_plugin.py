# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from garuda.core.models import GAPlugin

class GAAuthenticationPlugin(GAPlugin):
    """
    """

    __metaclass__ = ABCMeta

    def should_manage(self, request):
        """
        """
        return True

    def extract_session_identifier(self, request):
        ""
        ""
        return

    @abstractmethod
    def authenticate(self, request):
        """
        """
        pass