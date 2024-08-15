from django.contrib.auth.views import LogoutView

from django.urls import path

from users.views import (
    RegisterView,
    CustomLoginView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    ProfileUpdateView,
)
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_done",
    ),
]
