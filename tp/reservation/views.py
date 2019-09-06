# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from reservation.models import ParkingSpace
from django.core import serializers
from .serializers import CostSerializer, CancelSerializer, BookSerializer, EndSerializer
from rest_framework.authentication import TokenAuthentication

class BookView(APIView):
    """
    This API is used for booking parking space
    :method: POST 
    """

    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parking = serializer.validated_data["parking"]
        booked_time = serializer.validated_data["booked_time"]
        return Response({"booked_time": booked_time, 'parking no':parking}, status=200)
#
class CancelView(APIView):
    """
        This API is used for cancelled booking parking space
        :method: POST 
        """
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        serializer = CancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"cancelled": serializer.validated_data['cancelled']}, status=200)

class EndView(APIView):
    """
        This API is used for end booking parking space
        :method: POST 
        """
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        serializer = EndSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"booking_ended_time": serializer.validated_data['finished']}, status=200)

class CostView(APIView):
    """
        This API is used for get the cost per hour of booking parking space
        :method: POST 
        """
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        serializer = CostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cost = serializer.validated_data["cost"]
        return Response({"cost_per_hour": cost}, status=200)



class AvailableView(APIView):
    """
        This API is used for getting available parking space
        :method: GET 
        """

    def get(self, request):
        parking_list = ParkingSpace.objects.filter(is_open=True)
        data = serializers.serialize("json", parking_list)

        return Response({"available": data}, status=200)

