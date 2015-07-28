from copy import deepcopy


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


class Action(object):
    """

    """
    PRE_CREATE  = 0
    POST_CREATE = 1
    PRE_UPDATE  = 2
    POST_UPDATE = 3