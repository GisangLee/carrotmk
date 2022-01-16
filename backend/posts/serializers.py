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
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = post_models.Post
        fields = ["pk", "author", "title", "desc", "images"]


class PostModifySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = post_models.Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    photos = serializers.SerializerMethodField()

    class Meta:
        model = post_models.Post
        fields = "__all__"

    def get_photos(self, obj):
        return [PhotoSerializer(x).data for x in obj.photos.all()]
