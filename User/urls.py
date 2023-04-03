from django.urls import path

from .views import (
    register,
    Logout,
    oauth_test
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'User'

urlpatterns = [
    path('register/', register, name="Register"),
    path('login/', obtain_auth_token, name="Login"),
    path('logout/', Logout.as_view(), name="Logout"),
    path('login/google/oauth2callback/', oauth_test, name="OAuthTest")
]