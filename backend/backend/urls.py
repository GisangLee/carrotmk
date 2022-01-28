from os import stat
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("posts/", include("posts.urls", namespace="posts")),
    path("baton/", include("baton.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:

    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
