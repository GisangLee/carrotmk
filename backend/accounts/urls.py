from django.urls import path
from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path("signup/", accounts_views.SignupView.as_view()),
]
