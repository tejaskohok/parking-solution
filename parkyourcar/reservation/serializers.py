from rest_framework import serializers

from .models import ParkingSpace, Reservation

class parkingSpaceSerializers(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpace
        fields = ("name", "lat", "long", "hourly_rate", "zipcode", "available_slots")


class reservationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__" # ("reservation_id", "user", "parking_space_id", "status", "reserve_from_time")
