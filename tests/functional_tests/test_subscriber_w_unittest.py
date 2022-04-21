import pprint
import re
import sys
import unittest
from collections import OrderedDict
from unittest import TestCase
from subscriber.subscriber_data import SubscriberData
from tests.tstextra.test_data_generator import FakeNameAddressPhoneEmailStream

class SubscriberDataFunctionalTest(TestCase):
    """Sample functional test using Python's unittest framework"""
    def setUp(self) -> None:
        self.sdb = SubscriberData("mongodb://localhost:27017/")
        self.subscriber_src = FakeNameAddressPhoneEmailStream()
        self.test_subscribers = []
        for i, subscriber in enumerate(self.subscriber_src.records()):
            self.test_subscribers.append(subscriber)
            if i == 3:
                break
        self.added_records = []
    
    def test_subscriber_crud(self):
        for i in range(len(self.test_subscribers)):
            id = self.sdb.add_subscriber("usa", self.test_subscribers[i])
            self.assertRegex(id, r"[0-9a-fA-F]{24,24}", "id not 24 digit hex string")
            self.added_records.append(id)
        
    def tearDown(self) -> None:
        self.sdb.delete_subscribers("usa", self.added_records)
        self.sdb.close()
        
    def runTest(self):
        """This method is for debugging - not needed for normal auto-test discovery"""
        self.test_subscriber_crud()

