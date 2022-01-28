import os
import requests
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models as user_models
from . import serializers as user_serializers


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


class KakaoException(Exception):
    pass


class KakaoLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
        print(f"rest_api_key : {rest_api_key}")
        callback_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"
        redirect_uri = f"kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={callback_uri}&response_type=code"
        return redirect(f"https://{redirect_uri}")


class KakaoCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
        callback_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"
        code = request.GET.get("code")

        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={callback_uri}&code={code}"
        )

        token_response_json = token_request.json()
        print(f"토큰 정보 : {token_response_json}")
        access_token = token_response_json.get("access_token")
        print(f"액세스 토큰 : {access_token}")

        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()

        print(f"프로필 정보 : {profile_json}")

        email = profile_json.get("kakao_account").get("email", None)

        properties = profile_json.get("properties")

        nickname = properties.get("nickname")
        gender = profile_json.get("kakao_account").get("gender")
        profile_image = profile_json.get("kakao_account")
        profile_image = profile_image.get("profile").get("profile_image_url")

        if gender == "male":
            gender = "남자"
        elif gender == "female":
            gender = "여자"

        print(f"성별 : {gender}")
        print(f"프로필 이미지 : {profile_image}")

        try:
            user = user_models.User.objects.get(email=email)
            if user:
                raise KakaoException("이미 존재하는 사용자 입니다.")

        except user_models.User.DoesNotExist:
            user = user_models.User.objects.create(
                email=email, username=nickname, gender=gender
            )

            jwt_token = user_serializers.JwtTokenObtainSerializer.get_token(user)
            refresh_token = str(jwt_token)
            access_token = str(jwt_token.access_token)

            user.refresh_jwt_token = refresh_token
            user.set_unusable_password()
            user.save()

            response = {
                "message": "success",
                "token": access_token,
                "user": user.username,
            }

            return Response(response, status=status.HTTP_200_OK)
