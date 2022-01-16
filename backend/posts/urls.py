from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("posts/", views.PostListView.as_view()),
    path("post/upload", views.PostCreateView.as_view()),
    path("post/<int:pk>/", views.PostModifyView.as_view()),
]
