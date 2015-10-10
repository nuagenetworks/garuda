# -*- coding: utf-8 -*-

class GAPlugin(object):
    """
    """

    def __init__(self):
        """
        """
        self.core_controller = None

    def will_register(self):
        """
        """
        pass

    def did_register(self):
        """
        """
        pass

    def will_unregister(self):
        """
        """
        pass

    def did_unregister(self):
        """
        """
        pass

    @classmethod
    def manifest(cls):
        """
        """
        raise NotImplemented("manifest method must be implemented")