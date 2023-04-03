"""AuthTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from allauth.socialaccount.providers.google import views as google_view

from rest_framework.authtoken import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from User.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('google_login/', google_view.oauth2_login, name="Google"),
    path('test/', include('allauth.urls')),

    path('user/', include('User.urls')),
    path('book/', include('Book.urls'))
]
