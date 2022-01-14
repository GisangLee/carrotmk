from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as user_models

# Register your models here.


@admin.register(user_models.User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ["pk", "username", "email", "email_verified", "gender"]

    fieldsets = (
        ("유저 기본 정보", {"fields": ("avatar", "gender",),}),
    ) + UserAdmin.fieldsets

