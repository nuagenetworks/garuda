# -*- coding: utf-8 -*-


class GAConfig(object):
    """
    """

    # Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'
    REDIS_DB = 0

    # Format
    DATE_FORMAT = '%Y-%m-%d %H %M %S %f'

    # VSD
    VSD_USERNAME = 'csproot'
    VSD_PASSWORD = 'csproot'
    VSD_ENTERPRISE = 'csp'
    VSD_API_URL = 'https://135.227.222.46:8443'

    # Push notification
    PUSH_TIMEOUT = 5
