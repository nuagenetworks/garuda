# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

import logging
sdk_logger = logging.getLogger("tstdk")

def set_log_level(level, handler=None):
    """ Set both tstdk and Bambou log level to the given level

        Args:
            level (logging.level): a logging level
            handler (logging.Handler): a logging handler

        Notes:
            if no handler is provided, it will automatically create a new StreamHandler.

        Examples:
            >>> set_log_level(logging.INFO)
            >>> set_log_level(logging.DEBUG, logging.Streamhandler())
            >>> set_log_level(logging.ERROR)

    """

    from bambou import bambou_logger, pushcenter_logger

    if handler is None:
        handler = logging.StreamHandler()

    bambou_logger.setLevel(level)
    bambou_logger.addHandler(handler)

    pushcenter_logger.setLevel(level)
    pushcenter_logger.addHandler(handler)

    sdk_logger.setLevel(level)
    sdk_logger.addHandler(handler)