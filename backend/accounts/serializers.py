from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from . import models as user_models


class JwtTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(JwtTokenObtainSerializer, cls).get_token(user)
        token["user_pk"] = user.pk
        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=320)
    password = serializers.CharField(max_length=128, write_only=True)
    refresh_jwt_token = serializers.CharField(max_length=500, read_only=True)

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
            jwt_token = JwtTokenObtainSerializer.get_token(user)
            refresh_token = str(jwt_token)
            access_token = str(jwt_token.access_token)
            token = {"refresh_token": refresh_token, "access_token": access_token}
            update_last_login(None, user)
        except user_models.User.DoesNotExist:
            raise serializers.ValidationError("User does not exists")

        return {
            "username": user.pk,
            "token": token,
        }

    def create(self, validated_data):
        print("인증 값 : ", validated_data)
        pk = validated_data["username"]
        refresh_token = validated_data["token"]["refresh_token"]
        if refresh_token:
            user = user_models.User.objects.get(pk=pk)
            user.refresh_jwt_token = refresh_token
            user.save()
            return user


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
