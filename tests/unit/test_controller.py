from unittest import TestCase
import redis

from garuda.core.controllers import GACoreController
from garuda.core.models import GAController

class FakeController(GAController):

    def __init__(self, core_controller):
        super(FakeController, self).__init__(core_controller=core_controller)
        self.is_ready = False
        self.is_started = False

    def ready(self):
        self.is_ready = True

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    @classmethod
    def identifier(cls):
        return 'the.id'


class TestController(TestCase):
    """
    """
    def test_init_without_core_controller(self):
        """
        """
        with self.assertRaises(RuntimeError):
            controller = GAController(core_controller=None)

    def test_identifier_must_be_implemented(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))
        with self.assertRaises(NotImplementedError):
            controller.identifier()

        with self.assertRaises(NotImplementedError):
            controller.__class__.identifier()

    def test_redis_informations(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))

        self.assertEquals(controller.subscriptions, {})
        self.assertEquals(controller.redis_host, '127.0.0.1')
        self.assertEquals(controller.redis_port, 6379)
        self.assertEquals(controller.redis_db, 6)

    def test_uuid(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))

        self.assertIsNotNone(controller.uuid)

    def test_ready(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))
        controller.ready()

    def test_start(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))
        controller.start()

    def test_stop(self):
        """
        """
        controller = GAController(core_controller=GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}))
        controller.stop()

    def test_lifecycle(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        self.assertIsNotNone(controller)
        self.assertFalse(controller.is_started)
        self.assertTrue(controller.is_ready)

        core_controller.start()
        self.assertTrue(controller.is_started)
        self.assertTrue(controller.is_ready)

        core_controller.stop()
        self.assertFalse(controller.is_started)
        self.assertTrue(controller.is_ready)

    def test_start_stop_twice(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        controller.start_listening_to_events()
        thread = controller._pubsub_thread
        controller.start_listening_to_events()
        self.assertEquals(controller._pubsub_thread, thread)

        controller.stop_listening_to_events()
        controller.stop_listening_to_events()

        self.assertIsNone(controller._pubsub_thread)

    def test_offline_subscriptions(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        def handler(data):
            pass

        controller.subscribe('test-channel1', handler)
        controller.subscribe('test-channel2', handler)

        self.assertEquals(controller.subscriptions['test-channel1'], handler)
        self.assertEquals(controller.subscriptions['test-channel2'], handler)

        self.assertTrue('test-channel1' in controller.subscriptions)
        self.assertTrue('test-channel2' in controller.subscriptions)

        controller.unsubscribe('test-channel1')
        controller.unsubscribe('test-channel2')

        self.assertEquals(len(controller.subscriptions), 0)
        self.assertFalse('test-channel1' in controller.subscriptions)
        self.assertFalse('test-channel2' in controller.subscriptions)

    def test_online_subscriptions(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        def handler(data):
            pass

        controller.start_listening_to_events()
        controller.subscribe('test-channel1', handler)
        controller.subscribe('test-channel2', handler)

        self.assertTrue('test-channel1' in controller.subscriptions)
        self.assertTrue('test-channel2' in controller.subscriptions)

        controller.unsubscribe('test-channel1')
        controller.unsubscribe('test-channel2')
        controller.stop_listening_to_events()

        self.assertFalse('test-channel1' in controller.subscriptions)
        self.assertFalse('test-channel2' in controller.subscriptions)

    def test_mixed_subscriptions(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        def handler(data):
            pass

        controller.subscribe('test-channel1', handler)
        controller.start_listening_to_events()
        controller.subscribe('test-channel2', handler)

        self.assertTrue('test-channel1' in controller.subscriptions)
        self.assertTrue('test-channel2' in controller.subscriptions)

        controller.unsubscribe('test-channel1')
        controller.stop_listening_to_events()
        controller.unsubscribe('test-channel2')

        self.assertFalse('test-channel1' in controller.subscriptions)
        self.assertFalse('test-channel2' in controller.subscriptions)


    def test_unsubscribe_all_online(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        def handler(data):
            self.assertEquals(data, 'hello')

        controller.start_listening_to_events()
        controller.subscribe('test-channel1', handler)
        controller.subscribe('test-channel2', handler)

        self.assertTrue('test-channel1' in controller.subscriptions)
        self.assertTrue('test-channel2' in controller.subscriptions)

        controller.unsubscribe_all()
        controller.stop_listening_to_events()

        self.assertFalse('test-channel1' in controller.subscriptions)
        self.assertFalse('test-channel2' in controller.subscriptions)

    def test_publish(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')

        def handler(data):
            self.assertEquals(data, 'hello')

        core_controller.start()
        controller.subscribe('test-channel', handler)
        controller.start_listening_to_events()
        controller.publish('test-channel', 'hello')
        controller.stop_listening_to_events()
        core_controller.stop()

    def test_stop_listening_to_events_when_not_listening(self):
        """
        """
        core_controller = GACoreController( garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[FakeController])
        controller = core_controller.additional_controller(identifier='the.id')
        controller.stop_listening_to_events()