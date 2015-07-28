# -*- coding: utf-8 -*-

from utils import DisagreementReason


class MyPlugin(object):
    """

    """
    def precreate_callback(self, context):
        print 'Pre-callback 1'

        return context

    def precreate_callback2(self, context):
        print 'Pre-callback 2'
        # context.disagreement_reasons.append(DisagreementReason(origin=self, reason='500 is not a real crash', suggestion='Activates your statistics server'))

        return context

    def postcreate_callback(self, context):
        print 'Post-callback 1'
        context.disagreement_reasons.append(DisagreementReason(origin=self, reason='Something wrong happened', suggestion='Try again after 120s... just kidding'))
        return context

    def postcreate_callback2(self, context):
        print 'Post-callback 2'

        return context