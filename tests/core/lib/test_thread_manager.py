from unittest import TestCase

from garuda.core.lib import ThreadManager


class TestThreadManager(TestCase):
    """
    """

    def test_pool(self):
        """
        """
        def test(number):
            number += 10
            return number

        thread_manager = ThreadManager(size=2)
        results = thread_manager.start(test, [1, 2, 3])

        self.assertEquals(results, [11, 12, 13])

    def test_stop_pool(self):
        """
        """
        def test(number):
            import time
            time.sleep(1000)

        thread_manager = ThreadManager(size=2)
        thread_manager.start(test, [1, 2, 3], async=True)
        thread_manager.stop_all()
