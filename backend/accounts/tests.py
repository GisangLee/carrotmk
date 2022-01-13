import json
from django.test import TestCase, Client
from django.urls import reverse
import rest_framework
from accounts import models as user_models

# Create your tests here.

client = Client()


class SignupTest(TestCase):
    def test_signup_post_success(self):
        data = {
            "username": "test0710",
            "email": "test0710@naver.com",
            "password": "rltkd123",
            "gender": "남자",
        }

        response = client.post(
            "/accounts/signup/", json.dumps(data), content_type="application/json"
        )

        print(f"res data : {response.data}")
        print(f"res json : {response.json()}")

        self.assertEqual(
            response.json(),
            {
                "pk": response.data["pk"],
                "username": "test0710",
                "email": "test0710@naver.com",
                "gender": "남자",
            },
        )

        self.assertEqual(response.status_code, 201)


class LoginTest(TestCase):
    def test_login_jwt_post_success(self):

        data = {"username": "dev", "password": "rltkd123"}

        response = client.post(
            "/accounts/token/auth/", json.dumps(data), content_type="application/json"
        )

        print(f"res : {response.data}")

        self.assertEqual(
            response.json(), {"message": "success", "token": response.data["token"]}
        )

