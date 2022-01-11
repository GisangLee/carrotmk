from os import set_inheritable
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    response = None
    res_status = None

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)

        if not serializer.is_valid():
            response = {"message": "Request Body Error"}
            res_status = status.HTTP_409_CONFLICT

        elif serializer.validated_data["username"] == None:
            response = {"message": "fail"}
            res_status = status.HTTP_200_OK
        else:
            response = {"message": "success", "token": serializer.data["token"]}
            res_status = status.HTTP_200_OK
        return Response(response, status=res_status)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
