from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import models as post_models
from . import serializers

# Create your views here.


class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        posts = post_models.Post.objects.all()
        serializer = serializers.PostListSerializer(posts, many=True)
        print(f"serializer data : {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)

