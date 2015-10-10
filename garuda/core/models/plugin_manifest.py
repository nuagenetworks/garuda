# -*- coding: utf-8 -*-


class GAPluginManifest(object):
    """

    """

    def __init__(self, name, version, identifier, subscriptions=None):
        """
        """
        self.name = name
        self.subscriptions = subscriptions
        self.version = version
        self.identifier = identifier
