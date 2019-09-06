# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from login.models import Profile
# Create your models here.

class ParkingSpace(models.Model):
    parking_space_number = models.CharField(max_length=4)
    long = models.DecimalField(max_digits=8,decimal_places=2, null=True, blank=True)
    lat = models.DecimalField(max_digits=8,decimal_places=2, null=True, blank=True)
    cost_per_hour = models.DecimalField(max_digits=8,decimal_places=2)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.parking_space_number) + ": "+ str(self.is_open)


class Reservation(models.Model):

    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    parking_space = models.OneToOneField(ParkingSpace, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.now)
    finish_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, default="FREE")

    def __str__(self):
        return str(self.parking_space.parking_space_number) + ": "+ str(self.user.profile.phone_number)

