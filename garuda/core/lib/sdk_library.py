# -*- coding:utf-8 -*-

import logging
logger = logging.getLogger('garuda.sdksmanager')

from garuda.core.lib import SDKTransformer
from bambou import NURESTModelController
from garuda.core.lib import Singleton
from collections import OrderedDict


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
        if not identifier in self._sdks:
            logger.error("SDK version not found for identifier"  % identifier)
            return None

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

        if sdk is None:
            return None

        sdkinfo = getattr(sdk, 'SDKInfo', None)

        if sdkinfo:
            klass = getattr(sdkinfo, information_name, None)
            logger.info("SDK %s defines %s %s" % (sdk, information_name,  klass))
            return klass()

        logger.warn("SDK %s does not provide SDKInfo class" % sdk)
        return None

    def get_instance(self, resource_name, **attributes):
        """
        """
        rest_name = SDKTransformer.get_singular_name(resource_name)
        klass = NURESTModelController.get_first_model(rest_name)

        if klass:
            python_attributes = dict()

            for attribute_name, attribute_value in attributes.iteritems():
                python_name = SDKTransformer.get_python_name(attribute_name)
                python_attributes[python_name] = attribute_value

            return klass(**python_attributes)

        return None
