# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.core.exceptions import ValidationError
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from math import sin, cos, sqrt, atan2, radians
from .models import ParkingSpace, Reservation
from django.core.exceptions import ObjectDoesNotExist
from .serializers import ParkingSpaceSerializers, ReservationSerializers


class ParkingSpaceHandler(APIView):
    """ Class to handle request regarding parking spaces """

    DEFAULT_SEARCH_RADIUS = 5

    @classmethod
    def get_distance(cls, lat1, lon1, lat2, lon2):
        """ Function calculates and returns distance between two geo points in meters"""

        earth_radius = 6373.0  # approximate radius of earth in KM

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius * c

    def get(self, request):
        """ Function returns parking spaces with in given range """

        user_lat = float(request.query_params.get("latitude"))
        user_long = float(request.query_params.get("longitude"))
        search_radius = int(request.query_params.get("radius")) if request.query_params.get("radius") else \
            ParkingSpaceHandler.DEFAULT_SEARCH_RADIUS

        parking_spaces = [parking_space for parking_space in ParkingSpace.objects.all()
                          if ParkingSpaceHandler.get_distance(user_lat, user_long, parking_space.lat,
                                                              parking_space.long) <= search_radius
                          and parking_space.available_slots > 0]

        serializer = ParkingSpaceSerializers(parking_spaces, many=True)
        return Response(serializer.data)


class ReservationHandler(APIView):
    """ Class to handle requests regarding parking space reservation """

    def get(self, request, user_id):
        """ Function to view reservations of a given user """
        reservation = Reservation.objects.filter(user_id=user_id)
        serializer = ReservationSerializers(reservation, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Function to handle new reservation request """
        requested_parking_space_id = request.data.get("parking_space_id")
        try:  # Validate parking space
            parking_space = ParkingSpace.objects.get(parking_space_id=requested_parking_space_id)
        except ObjectDoesNotExist:
            response = json.dumps({"error": "Invalid parking space ID {}".format(requested_parking_space_id)})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if parking_space.available_slots == 0:
            response = json.dumps(
                {"error": "No parking spot available in the parking space {}".format(parking_space.name)})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate reservation time format
            reservation_time = datetime.datetime.strptime(request.data.get("reserve_from_time"), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            response = json.dumps({"error": "Reservation time needs to be in format 'YYYY-MM-DD HH:MM:SS'"})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if reservation_time < datetime.datetime.now():  # Validate reservation time
            response = json.dumps({"error": "Reservation time is prior to current time"})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReservationSerializers(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            parking_space = ParkingSpace.objects.get(parking_space_id=instance.parking_space_id_id)
            parking_space.available_slots -= 1  # Reduce available slots
            parking_space.save()
            # Get cost of parking
            response = json.dumps({"hourly_cost": parking_space.hourly_rate})

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, reservation_id):
        """ Function to handle cancel reservation request"""
        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reservation.status = "Canceled"  # Set status as 'Canceled'
        reservation.save()

        canceled_reservation = json.dumps(
            {"user": reservation.user.username, "reservation_id": reservation.reservation_id,
             "status": reservation.status})
        response = Response(canceled_reservation, status=status.HTTP_204_NO_CONTENT)
        return response
