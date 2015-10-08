# -*- coding: utf-8 -*-

class GAPlugin(object):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        raise NotImplemented("information method must be implemented")

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