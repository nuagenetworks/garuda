# -*- coding: utf-8 -*-

class GAPlugin(object):
    """
    """

    def __init__(self): # pragma: no cover
        """
        """
        self.core_controller = None

    def will_register(self): # pragma: no cover
        """
        """
        pass

    def did_register(self): # pragma: no cover
        """
        """
        pass

    def will_unregister(self): # pragma: no cover
        """
        """
        pass

    def did_unregister(self): # pragma: no cover
        """
        """
        pass

    @classmethod
    def manifest(cls): # pragma: no cover
        """
        """
        raise NotImplementedError("manifest method must be implemented")