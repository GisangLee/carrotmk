from os import set_inheritable
from django.shortcuts import render
from django.contrib.auth import logout
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
        print("serializer : ", serializer)

        if not serializer.is_valid():

            response = {"message": "Request Body Error", "token": None}
            res_status = status.HTTP_409_CONFLICT

        elif serializer.validated_data["username"] == None:

            response = {"message": "fail", "token": None}
            res_status = status.HTTP_200_OK
        else:
            print("validated_data", serializer.validated_data)
            print("\n")

            refresh_token = serializer.validated_data["token"]["refresh_token"]
            access_token = serializer.validated_data["token"]["access_token"]

            response = {
                "message": "success",
                "token": access_token,
                "user": serializer.validated_data["username"],
            }

            print(f"request.session.session_key : {request.session.session_key}")
            serializer.save(refresh_jwt_token=refresh_token)
            res_status = status.HTTP_200_OK

        return Response(response, status=res_status)


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = serializers.SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(
                f"response: {Response(serializer.data, status=status.HTTP_201_CREATED)}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request, format=None):
        print("로그아웃 중=============")
        logout(request)
        print("로그아웃 완료===============")
        return Response(status=status.HTTP_200_OK)
