import logging
import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db import transaction
from django.contrib.auth import logout
from django.contrib.auth.models import Group

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import UserRegistrationSerializer

log = logging.getLogger('main')


@api_view(["POST"])
@transaction.atomic()
@permission_classes([AllowAny])
@extend_schema(responses=UserRegistrationSerializer)
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        json_string = json.dumps(serializer.validated_data, default=str)
        log.debug("New User: " + json_string)

        user = serializer.save()

        if serializer.data["designation"] == "T":
            group = Group.objects.get(name='Teacher')
            user.groups.add(group)
        else:
            group = Group.objects.get(name='Student')
            user.groups.add(group)

        data = serializer.validated_data
        data["token"] = Token.objects.get_or_create(user=user)[0].key

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        json_string = json.dumps(request.data, default=str)
        log.error("Validation Error: " + json_string)

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class Logout(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({"message": "User Logged Out"}, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/user/login/google/oauth2callback/"
    client_class = OAuth2Client


def oauth_test(request):
    return render(request, "OAuth Test.html", {})
