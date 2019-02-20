from rest_framework import serializers

from .models import ParkingSpace, Reservation


class ParkingSpaceSerializers(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = ("name", "lat", "long", "hourly_rate", "zip_code", "available_slots")


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"  # ("reservation_id", "user", "parking_space_id", "status", "reserve_from_time")
