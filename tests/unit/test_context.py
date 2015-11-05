from unittest import TestCase

from garuda.core.models import GAContext, GARequest, GAResponseSuccess, GAResponseFailure, GASession, GAError, GAPushEvent

from tests.tstdk import v1_0 as tstdk


class TestContext(TestCase):
    """
    """

    def test_initialization(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)

        self.assertEquals(len(context.objects), 0)
        self.assertEquals(context.object, None)
        self.assertEquals(context.parent_object, None)
        self.assertEquals(context.request, request)
        self.assertEquals(context.session, session)
        self.assertEquals(len(context.errors), 0)
        self.assertEquals(context.has_errors, False)
        self.assertEquals(len(context.events), 0)
        self.assertEquals(context.has_events, False)

    def test_add_errors(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)
        error1 = GAError(type=GAError.TYPE_INVALID, title='title1', description='description2', suggestion='nope', property_name='prop1')
        error2 = GAError(type=GAError.TYPE_CONFLICT, title='title2', description='description3', suggestion='nope', property_name='prop2')
        error3 = GAError(type=GAError.TYPE_NOTFOUND, title='title3', description='description4', suggestion='nope', property_name='prop3')

        context.add_error(error1)
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.has_errors, True)

        context.add_errors([error2, error3])
        self.assertEquals(len(context.errors), 3)
        self.assertEquals(context.has_errors, True)

    def test_clear_errors(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)
        error1 = GAError(type=GAError.TYPE_INVALID, title='title1', description='description2', suggestion='nope', property_name='prop1')
        error2 = GAError(type=GAError.TYPE_CONFLICT, title='title2', description='description3', suggestion='nope', property_name='prop2')
        error3 = GAError(type=GAError.TYPE_NOTFOUND, title='title3', description='description4', suggestion='nope', property_name='prop3')

        context.add_errors([error1, error2, error3])
        self.assertEquals(len(context.errors), 3)
        self.assertEquals(context.has_errors, True)

        context.clear_errors()
        self.assertEquals(len(context.errors), 0)
        self.assertEquals(context.has_errors, False)

    def test_add_events(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)
        event1 = GAPushEvent(action=GARequest.ACTION_UPDATE, entity=tstdk.GAEnterprise())
        event2 = GAPushEvent(action=GARequest.ACTION_CREATE, entity=tstdk.GAEnterprise())
        event3 = GAPushEvent(action=GARequest.ACTION_DELETE, entity=tstdk.GAEnterprise())

        context.add_event(event1)
        self.assertEquals(len(context.events), 1)
        self.assertEquals(context.has_events, True)

        context.add_events([event2, event3])
        self.assertEquals(len(context.events), 3)
        self.assertEquals(context.has_events, True)

    def test_clear_events(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)
        event1 = GAPushEvent(action=GARequest.ACTION_UPDATE, entity=tstdk.GAEnterprise())
        event2 = GAPushEvent(action=GARequest.ACTION_CREATE, entity=tstdk.GAEnterprise())
        event3 = GAPushEvent(action=GARequest.ACTION_DELETE, entity=tstdk.GAEnterprise())

        context.add_events([event1, event2, event3])
        self.assertEquals(len(context.events), 3)
        self.assertEquals(context.has_events, True)

        context.clear_events()
        self.assertEquals(len(context.events), 0)
        self.assertEquals(context.has_events, False)

    def test_copy(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)

        context.add_error(GAError(type=GAError.TYPE_INVALID, title='title1', description='description2', suggestion='nope', property_name='prop1'))
        context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='title2', description='description3', suggestion='nope', property_name='prop2'))
        context.add_error(GAError(type=GAError.TYPE_NOTFOUND, title='title3', description='description4', suggestion='nope', property_name='prop3'))
        context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=tstdk.GAEnterprise()))
        context.add_event(GAPushEvent(action=GARequest.ACTION_CREATE, entity=tstdk.GAEnterprise()))
        context.add_event(GAPushEvent(action=GARequest.ACTION_DELETE, entity=tstdk.GAEnterprise()))

        context.object = tstdk.GAEnterprise(name='enterprise1')
        context.objects = [tstdk.GAEnterprise(name='enterprise2'), tstdk.GAEnterprise(name='enterprise3')]

        context_copy = context.copy()

        self.assertEquals(context_copy.session.uuid, session.uuid)
        self.assertEquals(context_copy.request.action, GARequest.ACTION_READ)
        self.assertEquals([obj.name for obj in context_copy.objects], [obj.name for obj in context.objects])
        self.assertEquals(context_copy.object.name, context.object.name)

        self.assertEquals(context_copy.has_errors, True)
        self.assertEquals(len(context_copy.errors), 3)

        self.assertEquals(context_copy.has_events, True)
        self.assertEquals(len(context_copy.events), 3)

    def test_make_response_with_errors(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)

        error1 = GAError(type=GAError.TYPE_INVALID, title='title1', description='description2', suggestion='nope', property_name='prop1')
        error2 = GAError(type=GAError.TYPE_CONFLICT, title='title2', description='description3', suggestion='nope', property_name='prop2')
        error3 = GAError(type=GAError.TYPE_NOTFOUND, title='title3', description='description4', suggestion='nope', property_name='prop3')
        context.add_errors([error1, error2, error3])

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseFailure)
        self.assertEquals(response.content, [error1, error2, error3])

    def test_make_response_for_read_all(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise2')
        context.objects = [enterprise1, enterprise2]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1, enterprise2])

    def test_make_response_for_read(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        context.object = [enterprise1]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1])

    def test_make_response_for_create(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_CREATE)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        context.object = [enterprise1]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1])

    def test_make_response_for_update(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        context.object = [enterprise1]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1])

    def test_make_response_for_delete(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_DELETE)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        context.object = [enterprise1]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1])

    def test_make_response_for_assign(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_ASSIGN)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        context.object = [enterprise1]

        response = context.make_response()

        self.assertEquals(response.__class__, GAResponseSuccess)
        self.assertEquals(response.content, [enterprise1])