from statistics import mode
from rest_framework import serializers
from . import models as post_models
from accounts import models as user_models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_models.Photo
        fields = ["file"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = [
            "pk",
            "username",
            "email",
            "gender",
            "avatar",
            "email_verified",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = post_models.Post
        fields = ["pk", "author", "title", "desc"]


class PostModifySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = post_models.Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    photos = serializers.SerializerMethodField()

    is_like = serializers.SerializerMethodField()

    class Meta:
        model = post_models.Post
        fields = [
            "pk",
            "author",
            "title",
            "desc",
            "created_at",
            "updated_at",
            "photos",
            "is_like",
        ]

    def get_photos(self, obj):
        return [PhotoSerializer(x).data for x in obj.photos.all()]

    def get_is_like(self, obj):
        user = obj.author
        return obj.like_user_set.filter(pk=user.pk).exists()
