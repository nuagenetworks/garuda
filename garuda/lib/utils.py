# -*- coding: utf-8 -*-

import logging


def create_logger(name):
    """
    """

    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
