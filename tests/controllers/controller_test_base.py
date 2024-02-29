# -*- coding: utf-8 -*-

"""
    tests.controllers.controller_test_base


"""

import unittest
from moesifapi.moesif_api_client import *
from ..test_helper import TestHelper
from ..http_response_catcher import HttpResponseCatcher

class ControllerTestBase(unittest.TestCase):

    """All test classes inherit from this base class. It abstracts out
    common functionality and configuration variables set up."""

    @classmethod
    def setUpClass(cls):
        """Class method called once before running tests in a test class."""
        cls.api_client = MoesifAPIClient("eyJhcHAiOiI1NjU6NDYzIiwidmVyIjoiMi4xIiwib3JnIjoiNjI4OjM2MCIsImlhdCI6MTcwNjc0NTYwMH0.KTkq3jzf7vTTDeszWF39n8EiDNM5-DX0ld1ASvinoi4")
        cls.request_timeout = 30
        cls.assert_precision = 0.01


    def setUp(self):
        """Method called once before every test in a test class."""
        self.response_catcher = HttpResponseCatcher()
        self.controller.http_call_back =  self.response_catcher
