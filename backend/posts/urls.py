from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("posts/", views.PostListView.as_view()),
    path("posts/<int:pk>/", views.PostModifyView.as_view()),
]
