from django.urls import path

from .views import register, login, logout, AuthenticatedUser, Permissions

urlpatterns = [
    path("register", register),
    path("login", login),
    path("user", AuthenticatedUser.as_view()),
    path("logout", logout),
    path("permissions", Permissions.as_view())
]
