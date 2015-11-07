# -*- coding: utf-8 -*-

__all__ = ['GAContext',
           'GAError',
           'GAPlugin',
           'GAPluginManifest',
           'GAPushEvent',
           'GAPushNotification',
           'GARequest',
           'GAResource',
           'GAResponseFailure',
           'GAResponseSuccess',
           'GASession',
           'GAController',
           'GAPluginController',
           'GASerializable']

from collections import namedtuple
GAResource = namedtuple('GAResource', ['name', 'value'])

from .controller import GAController
from .plugin_controller import GAPluginController
from .context import GAContext
from .errors import GAError
from .plugin import GAPlugin
from .plugin_manifest import GAPluginManifest
from .push_event import GAPushEvent
from .push_notification import GAPushNotification
from .request import GARequest
from .response import GAResponseFailure, GAResponseSuccess
from .session import GASession
from .serializable import GASerializable
