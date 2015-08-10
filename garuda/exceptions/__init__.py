# -*- coding: utf-8 -*-


class NotImplementedException(Exception):
    """
    """
    pass


class InternalInconsistencyException(Exception):
    """
    """
    pass


class GAException(Exception):
    pass


class NotFoundException(GAException):
    """
    """
    pass


class BadRequestException(GAException):
    """
    """
    pass


class ConflictException(GAException):
    """
    """
    pass


class ActionNotAllowedException(GAException):
    """
    """
    pass
