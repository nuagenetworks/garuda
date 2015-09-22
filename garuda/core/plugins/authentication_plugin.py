# -*- coding: utf-8 -*-

from .abstracts import GAPlugin


class GAAuthenticationPlugin(GAPlugin):
    """
    """
    def should_manage(self, username, password, enterprise):
        """
        """
        return True

    def authenticate_user(self, username, password, enterprise):
        """
        """
        raise NotImplementedError("%s should implement authenticate_user method" % self)
