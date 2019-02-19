# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from reservation.models import ParkingSpace, Reservation
from django.test import Client
from reservation.views import ParkingSpaceHandler
from django.core.urlresolvers import reverse
from decimal import Decimal
import datetime


class BookReservationAPITest(TestCase):
    """This class holds test cases for '/bookparking/' API"""
    ParkingSpaceObj = None

    @classmethod
    def setUpClass(cls):
        # Create dummy ParkingSpace
        cls.ParkingSpaceObj = ParkingSpace(name='TestParking', lat="18.5825", long="73.7835", slots=10,
                                           available_slots=10, zip_code=411027, hourly_rate=10)
        cls.ParkingSpaceObj.save()

    def setUp(self):
        self.user = User.objects.create_user("testuser", "testuser@test.com", "test")

    def test_reserve_pre_current_time_parking(self):
        """Reserve parking slot with time prior to current time"""

        post_data = {'parking_space_id': BookReservationAPITest.ParkingSpaceObj.parking_space_id, 'user': self.user,
                     'reserve_from_time': datetime.datetime.strptime('2019-02-10T19:44', '%Y-%m-%dT%H:%M'),
                     'status': 'Availed'}

        response = Client().post('/bookparking/', data=post_data)
        self.assertEqual(response.status_code, 400, "Repsonse code is {}".format(response.status_code))

    def tearDown(self):
        user = User.objects.get_by_natural_key('testuser')
        user.delete()

    @classmethod
    def tearDownClass(cls):
        cls.ParkingSpaceObj.delete()
