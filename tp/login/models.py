# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(max_length=10)

    def __str__(self):
        return "{0} - {1}".format(self.user.username, self.phone_number)
