# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import ParkingSpace, Reservation

admin.site.register(Reservation)
admin.site.register(ParkingSpace)
