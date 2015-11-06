# -*- coding:utf-8 -*-

import logging
from collections import OrderedDict

from singleton import Singleton

logger = logging.getLogger('garuda.sdklibrary')


class SDKLibrary(object):
    """
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        self._sdks = OrderedDict()

    # Methods

    def register_sdk(self, identifier, sdk):
        """
        """
        self._sdks[identifier] = sdk

    def unregister_sdk(self, identifier):
        """
        """
        if identifier in self._sdks:
            del self._sdks[identifier]

    def get_sdk(self, identifier):
        """
        """
        if identifier not in self._sdks:
            raise IndexError("SDK version not found for identifier %s"  % identifier)

        return self._sdks[identifier]

    def get_sdk_session_class(self, identifier):
        """
        """
        return self._get_sdk_info(identifier=identifier, information_name='session_class')

    def get_sdk_root_class(self, identifier):
        """
        """
        return self._get_sdk_info(identifier=identifier, information_name='root_object_class')

    # Utils

    def _get_sdk_info(self, identifier, information_name):
        """
        """
        sdk = self.get_sdk(identifier=identifier)

        sdkinfo = getattr(sdk, 'SDKInfo', None)

        if sdkinfo:
            klass = getattr(sdkinfo, information_name, None)
            logger.info("SDK %s defines %s %s" % (sdk, information_name, klass))
            return klass()

        logger.warn("SDK %s does not provide SDKInfo class" % sdk)  # pragma: no cover
        return None  # pragma: no cover
