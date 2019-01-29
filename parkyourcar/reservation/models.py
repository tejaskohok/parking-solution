# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class ParkingSpace(models.Model):
    """ Model class to store parking space """
    parking_space_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    long = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    slots = models.IntegerField(blank=False)
    hourly_rate = models.IntegerField(blank=False)
    zipcode = models.CharField(max_length=10, blank=False)
    available_slots = models.IntegerField(blank=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """ Model class to store parking reservation """

    RESERVATION_STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Availed', 'Availed')
    )
    reservation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    parking_space_id =  models.ForeignKey(ParkingSpace)
    status = models.CharField(max_length=10, choices=RESERVATION_STATUS_CHOICES, blank=False)
    reserve_from_time = models.DateTimeField(blank=False)
