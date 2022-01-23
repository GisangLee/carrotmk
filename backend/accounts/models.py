from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_MALE = "남자"
    GENDER_FEMALE = "여자"
    GENDER_CHOICES = ((GENDER_MALE, "남자"), (GENDER_FEMALE, "여자"))

    email = models.EmailField(max_length=320, verbose_name="이메일")
    avatar = models.ImageField(
        upload_to="profile/%Y/%m/%d", blank=True, verbose_name="프로필"
    )
    email_verified = models.BooleanField(default=False, verbose_name="이메일 인증 여부")
    gender = models.CharField(
        choices=GENDER_CHOICES, blank=True, max_length=2, verbose_name="성별"
    )
    email_secret = models.CharField(max_length=200, blank=True, verbose_name="이메일 인증 키")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일자")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일자")
    refresh_jwt_token = models.CharField(
        max_length=500, blank=True, verbose_name="JWT 갱신 토큰"
    )
