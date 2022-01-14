from dataclasses import fields
from rest_framework import serializers
from . import models as post_models
from accounts import models as user_models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_models.Photo
        fields = ["pk", "file", "caption"]


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
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = post_models.Post
        fields = "__all__"

    def get_photo(self, obj):
        return [PhotoSerializer(x).data for x in obj.photos.all()]

    def update(self, obj, validated_data):
        print(f"update PUT validated data : {validated_data}")
        post_photo = validated_data.pop("photo")
        print(f"update PUT w/o photo validated data : {validated_data}")
        post = post_models.Post.objects.filter(pk=obj.pk).update(**validated_data)
        post = post_models.Post.objects.get(pk=post)
        print(f"post : {post.photos.all()}")
        post_photo["post"] = post
        # photo = post_models.Photo.objects.filter(pk=post.photos.pk).update(**post_photo)
        photo = post_models.Photo.objects.all().update_or_create(**post_photo)
        print(f"post : {post}")
        print(f"photo : {photo}")
        return post

    def create(self, validated_data):
        print(f"validated data : {validated_data}")
        photo_obj = validated_data.pop("photo")

        post = post_models.Post.objects.create(**validated_data)
        post.save()

        photo_obj["post"] = post

        if photo_obj:
            photo = post_models.Photo.objects.create(**photo_obj)
            photo.save()

        return post
