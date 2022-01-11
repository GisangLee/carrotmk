from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views as accounts_views

app_name = "accounts"

urlpatterns = [
    path("signup/", accounts_views.SignupView.as_view()),
    path("token/auth/", accounts_views.LoginView.as_view()),
]
