from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models as post_models
from . import serializers

# Create your views here.


class PostModifyView(APIView):
    def put(self, request, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            post = get_object_or_404(post_models.Post, pk=pk)

            if post.author.pk == request.user.pk:
                post_photo = request.data["photo"]
                serializer = serializers.PostListSerializer(post, data=request.data)
                if serializer.is_valid():
                    serializer.save(author=request.user, photo=post_photo)
                    return Response(serializer.data, status=status.HTTP_200_OK)
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

    def post(self, request):

        serialzier = serializers.PostListSerializer(data=request.data)
        print(f"REQUEST data : {request.data}")
        print(f"REQUEST user : {request.user}")
        print(f"REQUEST photo : {request.data['photo']}")
        post_photo = request.data["photo"]
        if serialzier.is_valid():
            print(f"게시글 작성 serializer data : {serialzier.validated_data}")
            serialzier.save(author=request.user, photo=post_photo)
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

