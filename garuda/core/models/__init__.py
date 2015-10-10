# -*- coding: utf-8 -*-

__all__ = ['GAContext', 'GAError', 'GAErrorsList', 'GAPushEvent', 'GAPushNotification',  'GARequest', 'GAResource', 'GAResponse', 'GASession', 'GAPlugin', 'c']

from collections import namedtuple
GAResource = namedtuple('GAResource', ['name', 'value'])

from .plugin_manifest import GAPluginManifest

from .plugin import GAPlugin
from .context import GAContext
from .errors import GAError, GAErrorsList
from .push_event import GAPushEvent
from .push_notification import GAPushNotification
from .request import GARequest
from .response import GAResponse
from .session import GASession