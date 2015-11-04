# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment


__all__ = ['GAEnterprise', 'GAGroup', 'GARoot', 'GAUser', 'GATSTSession', 'GAAddress']

from .gaenterprise import GAEnterprise
from .gagroup import GAGroup
from .garoot import GARoot
from .gauser import GAUser
from .gaadress import GAAddress
from .gatstsession import GATSTSession
from .sdkinfo import SDKInfo

def __setup_bambou():
    """ Avoid having bad behavior when using importlib.import_module method
    """
    import pkg_resources
    from bambou import BambouConfig, NURESTModelController

    default_attrs = pkg_resources.resource_filename(__name__, '/resources/attrs_defaults.ini')
    BambouConfig.set_default_values_config_file(default_attrs)

    NURESTModelController.register_model(GAEnterprise)
    NURESTModelController.register_model(GAGroup)
    NURESTModelController.register_model(GARoot)
    NURESTModelController.register_model(GAUser)
    NURESTModelController.register_model(GAAddress)


__setup_bambou()