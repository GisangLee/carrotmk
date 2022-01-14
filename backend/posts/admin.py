from django.contrib import admin
from . import models as post_models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = post_models.Photo


@admin.register(post_models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "file",
        "caption",
    )

    fieldsets = (("기본정보", {"fields": ("file", "caption", "post",),}),)


@admin.register(post_models.Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "pk",
        "author",
        "title",
        "desc",
    )

    inlines = (PhotoInline,)

    fieldsets = (("기본 정보", {"fields": ("author", "title", "desc",),}),)

