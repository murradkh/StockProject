from unittest import mock
import unittest
import os
from ..scheduler import scheduler


class Test_scheduler(unittest.TestCase):
    @mock.patch('os.urandom', side_effect=scheduler.start())
    def test_scheduler_job(self, urandom_function):
        assert os.urandom(3)
        assert urandom_function.called

