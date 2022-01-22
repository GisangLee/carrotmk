from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models as post_models
from . import serializers

# Create your views here.


class PhotoDeleteView(APIView):
    def delete(self, request, **kwargs):
        pk = kwargs.get("photo_pk")
        message = ""
        result = None

        if pk is not None:
            photo = get_object_or_404(post_models.Photo, pk=pk)
            if photo:
                message = "사진이 삭제 되었습니다."
                resulst = status.HTTP_200_OK
                photo.delete()
            else:
                message = "사진이 존재하지 않습니다."
                result = status.HTTP_400_BAD_REQUEST
        else:
            message = "사진이 존재하지 않습니다."
            result = status.HTTP_400_BAD_REQUEST
        return Response(message, status=result)


class PostModifyView(APIView):
    def put(self, request, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            post = get_object_or_404(post_models.Post, pk=pk)
            if post.author.pk == request.user.pk:
                photos = request.FILES.getlist("photos")
                if photos:
                    serializer = serializers.PostModifySerializer(
                        post, data=request.data
                    )
                    if serializer.is_valid():
                        post = serializer.save(author=request.user)
                        for photo in photos:
                            photo_obj = post_models.Photo.objects.create(
                                file=photo, post=post
                            )
                            photo_obj.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(
                            serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    serializer = serializers.PostModifySerializer(
                        post, data=request.data
                    )
                    if serializer.is_valid():
                        post = serializer.save(author=request.user)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)
        return Response("게시글이 존재하지 않습니다.", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get("pk")
        message = ""
        result = None

        if pk is not None:
            post = get_object_or_404(post_models.Post, pk=pk)
            if post:
                if post.author.pk == request.user.pk:
                    message = "게시글이 삭제되었습니다."
                    result = status.HTTP_200_OK
                    post.delete()
                else:
                    message = "권한이 없습니다."
                    result = status.HTTP_400_BAD_REQUEST
            else:
                message = "게시글이 존재하지 않습니다."
                result = status.HTTP_400_BAD_REQUEST
        else:
            message = "게시글이 존재하지 않습니다."
            result = status.HTTP_400_BAD_REQUEST

        return Response(message, status=result)


class PostCreateView(APIView):
    def post(self, request, format=None):
        serialzier = serializers.PostCreateSerializer(data=request.data)
        print(f"REQUEST data : {request.data}")
        print(f"REQUEST user : {request.user}")
        print(f"REQUEST FILES : {request.FILES}")

        photos = request.FILES.getlist("photos")
        if serialzier.is_valid():
            if photos:
                print("---------------사진 포함 게시글 작성 중....----------------")
                print(f"게시글 작성 serializer data : {serialzier.validated_data}")
                post = serialzier.save(author=request.user)
                print("게시글 저장")
                for photo in photos:
                    photos = post_models.Photo.objects.create(post=post, file=photo)
                    photos.save()
                return Response(serialzier.data, status=status.HTTP_201_CREATED)
            else:
                print("---------------사진  미포함 게시글 작성 중....----------------")
                print(f"게시글 작성 serializer data : {serialzier.validated_data}")
                post = serialzier.save(author=request.user)
                print("게시글 저장")
                return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        posts = (
            post_models.Post.objects.select_related("author")
            .prefetch_related("photos")
            .all()
        )
        serializer = serializers.PostListSerializer(posts, many=True)
        print(f"serializer data : {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)
