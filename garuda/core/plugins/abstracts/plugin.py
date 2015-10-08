# -*- coding: utf-8 -*-

class GAPlugin(object):
    """
    """

    @classmethod
    def manifest(self):
        """
        """
        raise NotImplemented("manifest method must be implemented")

    def __init__(self):
        """
        """
        self.manifest

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