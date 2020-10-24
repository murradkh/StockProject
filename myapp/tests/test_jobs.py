from unittest import mock
import unittest
import os
from ..scheduler.stock_api_update import stock_api_update


class Test_API(unittest.TestCase):
    @mock.patch('os.urandom', side_effect=stock_api_update())
    def test_job_api(self, urandom_function):
        assert os.urandom(3)
        assert urandom_function.called
