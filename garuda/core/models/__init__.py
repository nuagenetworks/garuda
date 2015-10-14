# -*- coding: utf-8 -*-

__all__ = ['GAContext',
           'GAError',
           'GAPlugin',
           'GAPluginManifest',
           'GAPushEvent',
           'GAPushEventQueue',
           'GAPushNotification',
           'GARequest',
           'GAResource',
           'GAResponseFailure',
           'GAResponseSuccess',
           'GASession']

from collections import namedtuple
GAResource = namedtuple('GAResource', ['name', 'value'])

from .context import GAContext
from .errors import GAError
from .plugin import GAPlugin
from .plugin_manifest import GAPluginManifest
from .push_event import GAPushEvent, GAPushEventQueue
from .push_notification import GAPushNotification
from .request import GARequest
from .response import GAResponseFailure, GAResponseSuccess
from .session import GASession
