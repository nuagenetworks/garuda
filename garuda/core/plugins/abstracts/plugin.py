# -*- coding: utf-8 -*-

class GAPlugin(object):
    """
    """

    def __init__(self, core_controller=None):
        """
        """
        self.core_controller = core_controller

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
    def manifest(self):
        """
        """
        raise NotImplemented("manifest method must be implemented")