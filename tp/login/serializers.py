from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import Profile
import random
import string

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['salary', 'designation', 'picture']


class EmployeeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'profile', 'email',
                  'is_staff', 'is_active', 'date_joined',
                  'is_superuser']


class LoginSerializer(serializers.Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phonenumber = data.get("phonenumber", "")
        password = data.get("password", "")
        if not phonenumber or len(phonenumber) != 10:
            msg = "Please check your phone number"
            raise exceptions.ValidationError(msg)

        profile = Profile.objects.get(phone_number=phonenumber)
        username=profile.user.username
        if password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide password both."
            raise exceptions.ValidationError(msg)
        return data


class SignupSerializer(serializers.Serializer):
    phonenumber = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        phonenumber = data.get("phonenumber", "")
        password = data.get("password", "")

        if not phonenumber or len(phonenumber) != 10:
            msg = "Please check your phone number"
            raise exceptions.ValidationError(msg)

        if not password:
            msg = "Please provide password"
            raise exceptions.ValidationError(msg)

        username=phonenumber+''.join(random.choice(string.lowercase) for x in range(2))
        user, created = User.objects.get_or_create(username=username)
        if not created:
            msg = "user already registered"
            raise exceptions.ValidationError(msg)
        if created:
            user.set_password(password)
            user.save()

        profile = Profile.objects.create(user=user, phone_number=phonenumber)
        data['user'] = user
        return data