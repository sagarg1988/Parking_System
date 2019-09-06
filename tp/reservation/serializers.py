from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from datetime import datetime
from .models import Reservation, ParkingSpace
from login.models import Profile

class CostSerializer(serializers.Serializer):
    parking_no = serializers.CharField()

    class Meta:
        model = ParkingSpace
        fields = ['parking_space_number']

    def validate(self, data):
        parking_no = data.get("parking_no", "")

        if not parking_no or int(parking_no) < 0:
            msg = "Please provide valid parking id"
            raise exceptions.ValidationError(msg)

        parking_list  = ParkingSpace.objects.filter(parking_space_number= parking_no)

        if len(parking_list)>1:
            msg = "multiple parking available for provided parking no"
            raise exceptions.ValidationError(msg)

        if not parking_list:
            msg = "Please check your parking number"
            raise exceptions.ValidationError(msg)

        data['cost'] = parking_list.last().cost_per_hour
        return data

class CancelSerializer(serializers.Serializer):
    parking_no = serializers.CharField()

    class Meta:
        model = ParkingSpace
        fields = ['parking_space_number']

    def validate(self, data):
        parking_no = data.get("parking_no", "")

        if not parking_no or int(parking_no) < 0:
            msg = "Please provide valid parking id"
            raise exceptions.ValidationError(msg)

        parking_list  = ParkingSpace.objects.filter(parking_space_number= parking_no)

        if len(parking_list)>1:
            msg = "multiple parking available for provided parking no"
            raise exceptions.ValidationError(msg)

        if not parking_list:
            msg = "Please check your parking number"
            raise exceptions.ValidationError(msg)

        parking = parking_list.last()

        if parking.is_open:
            msg = "Parking is open so can not cancel"
            raise exceptions.ValidationError(msg)

        booking = Reservation.objects.filter(parking_space=parking)

        now = datetime.now()

        if booking.status == "BOOKED":
            booking.status = "FREE"
            booking.finish_date = now
            booking.save()
            parking.is_open = True
            parking.save()
            data['cancelled'] = str(now)
        else:
            msg = "Can not cancel"
            raise exceptions.ValidationError(msg)

        return data


class BookSerializer(serializers.Serializer):
    parking_no = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = ParkingSpace
        fields = ['parking_space_number']

    def validate(self, data):
        parking_no = data.get("parking_no", "")
        phone_number = data.get("phone_number", "")

        if not parking_no or int(parking_no) < 0:
            msg = "Please provide valid parking id"
            raise exceptions.ValidationError(msg)

        parking_list = ParkingSpace.objects.filter(parking_space_number=parking_no)

        if len(parking_list) > 1:
            msg = "multiple parking available for provided parking no"
            raise exceptions.ValidationError(msg)

        if not parking_list:
            msg = "Please check your parking number"
            raise exceptions.ValidationError(msg)

        parking = parking_list.last()
        if not parking.is_open:
            msg = "Parking is open so can not book"
            raise exceptions.ValidationError(msg)

        profile = Profile.objects.get(phone_number=phone_number)
        now = datetime.now()
        booking = Reservation.objects.create(parking_space=parking, user=profile)
        booking.status = "BOOKED"
        booking.start_date = now
        booking.save()

        parking.is_open = False
        parking.save()
        data['parking'] = parking.id
        data['booked_time'] = now
        return data

class EndSerializer(serializers.Serializer):
    parking_no = serializers.CharField()

    class Meta:
        model = ParkingSpace
        fields = ['parking_space_number']

    def validate(self, data):
        parking_no = data.get("parking_no", "")

        if not parking_no or int(parking_no) < 0:
            msg = "Please provide valid parking id"
            raise exceptions.ValidationError(msg)

        parking_list = ParkingSpace.objects.filter(parking_space_number=parking_no)

        if len(parking_list) > 1:
            msg = "multiple parking available for provided parking no"
            raise exceptions.ValidationError(msg)

        if not parking_list:
            msg = "Please check your parking number"
            raise exceptions.ValidationError(msg)

        parking = parking_list.last()
        if parking.is_open:
            msg = "Parking is open so can not finish time"
            raise exceptions.ValidationError(msg)

        now = datetime.now()
        booking = Reservation.objects.filter(parking_space=parking).last()
        booking.status = "FREE"
        booking.finish_date = now
        booking.save()

        parking.is_open = True
        parking.save()
        data['parking'] = parking.id
        data['finished'] = now
        return data

class AvailableSerializer(serializers.Serializer):

    class Meta:
        model = ParkingSpace

    def validate(self, data):
        parking_no = data.get("parking_no", "")
        return data
