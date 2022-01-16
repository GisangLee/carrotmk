from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from . import models as user_models

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=320)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        print(f"username : {username}")
        print(f"password : {password}")
        print("user is ", user)

        if user is None:
            return {"username": None}

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except user_models.User.DoesNotExist:
            raise serializers.ValidationError("User does not exists")

        return {"username": user.pk, "token": jwt_token}


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["email"]:
            req_password = validated_data.pop("password")
            user = user_models.User.objects.create(**validated_data)
            user.set_password(req_password)
            user.save()
            return user

    class Meta:
        model = user_models.User
        fields = ["pk", "username", "email", "password", "gender"]
