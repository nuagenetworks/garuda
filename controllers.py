# -*- coding: utf-8 -*-

import gevent

from utils import Action, GAContext
from gaexceptions import InternalInconsistencyException


class CoreController(object):
    """

    """
    def __init__(self, session, request):
        """
        """
        self.context = GAContext(session=session, request=request)

    def do_the_job(self, *args, **kwargs):
        """

        """
        context = PluginController.execute_callbacks(action=Action.PRE_CREATE, context=self.context, *args, **kwargs)

        if len(context.disagreement_reasons) > 0:
            raise Exception('\n/!\ Plugin stopped before execution due to the following reasons:\n%s' % context.disagreement_reasons)

        ModelController.create(msg='Christophe')

        context = PluginController.execute_callbacks(action=Action.POST_CREATE, context=self.context, *args, **kwargs)

        if len(context.disagreement_reasons) > 0:
            raise Exception('\n/!\ Plugin stopped after execution due to the following reasons:\n%s' % context.disagreement_reasons)


class PluginController(object):
    """

    """
    timeout = 2
    _callbacks = None

    def _initialize_(f):
        def wrapper(cls, *args, **kwargs):
            if cls._callbacks is None:
                cls._callbacks = {Action.PRE_CREATE: [], Action.POST_CREATE: [], Action.PRE_UPDATE: [], Action.POST_UPDATE: []}

            return f(cls, *args, **kwargs)
        return wrapper

    @classmethod
    @_initialize_
    def register_callback(cls, action, callback):
        """

        """
        if action not in cls._callbacks:
            raise InternalInconsistencyException('Trying to register a callback with unknown action %s' % action)

        cls._callbacks[action].append(callback)

    @classmethod
    @_initialize_
    def remove_callback(cls, action, callback):
        """

        """
        if action not in cls._callbacks:
            raise InternalInconsistencyException('Trying to remove a callback with unknown action %s' % action)

        if callback not in cls._callbacks[action]:
            raise InternalInconsistencyException('Trying to remove an unknown callback %s' % callback)

        cls._callbacks[action].remove(callback)

    @classmethod
    def execute_callbacks(cls, action, context, *args, **kwargs):
        """

        """
        if action not in cls._callbacks:
            raise InternalInconsistencyException('Trying to execute callbacks for unknown action %s' % action)

        jobs = [gevent.spawn(callback, context=context.copy(), *args, **kwargs) for callback in cls._callbacks[action]]
        gevent.joinall(jobs, timeout=cls.timeout)

        context.merge_contexts([job.value for job in jobs])

        return context


class ModelController(object):
    """

    """
    @classmethod
    def create(cls, *args, **kwargs):
        """

        """
        print '** Let the police do the job **'
