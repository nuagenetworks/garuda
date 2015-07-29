# -*- coding: utf-8 -*-

from copy import deepcopy
from uuid import uuid4


class DisagreementReason(object):

    def __init__(self, origin, reason, suggestion=None):
        """

        """
        self.origin = origin
        self.reason = reason
        self.suggestion = suggestion

    def __repr__(self):
        """

        """
        return '<DisagreementReason> (origin=%s, reason=%s, suggestion=%s)' % (self.origin, self.reason, self.suggestion)


class GASession(object):
    """

    """
    def __init__(self):
        """

        """
        self.uuid = uuid4().hex
        self.resource = None
        self.user = None
        self.data = {}
        self.action = None


class GARequest(object):
    """

    """
    def __init__(self, method, url, data={}, headers={}, cookies=None):
        """
        """
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.cookies = cookies

class GAResponse(object):
    """

    """
    def __init__(self, status_code, data, headers={}):
        """
        """
        self.status_code = status_code
        self.data = data
        self.headers = headers

class GAContext(object):
    """

    """
    def __init__(self, session, request):
        """
        """
        self.disagreement_reasons = []
        self.session = session
        self.request = request

    def copy(self):
        """

        """
        return deepcopy(self)

    def merge_contexts(self, contexts):
        """

        """
        for context in contexts:
            if len(context.disagreement_reasons) > 0:
                self.disagreement_reasons += context.disagreement_reasons

            # TODO: Merge context object here...
            # Add the conflict in disagreement_reasons

            # Merge user_info