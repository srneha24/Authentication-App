import logging

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import BookSerializer
from .models import Book
from User.models import CustomUser


# Create your views here.

log = logging.getLogger('main')


class CreateBookView(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Book.objects.all()

    @extend_schema(responses=BookSerializer)
    @transaction.atomic()
    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            user = CustomUser.objects.get(email=request.user)
            serializer.set_user(user)
            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request):

        user = CustomUser.objects.get(email=request.user)

        if user.designation == "S":
            book = Book.objects.all()
            serializer = BookSerializer(book, many=True)

            return Response(serializer.data, status=status.HTTP_302_FOUND)
        else:
            book = Book.objects.filter(user=user)
            serializer = BookSerializer(book, many=True)

            return Response(serializer.data, status=status.HTTP_302_FOUND)


class BookView(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Book.objects.all()

    @extend_schema(responses=BookSerializer)
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)

        return Response(serializer.data, status=status.HTTP_302_FOUND)

    @extend_schema(responses=BookSerializer)
    @transaction.atomic()
    def patch(self, request, book_id):
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book, data=request.data)

        if book.user == request.user:
            if serializer.is_valid():
                user = CustomUser.objects.get(email=request.user)
                serializer.set_user(user)
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
        else:
            return Response({"message": "Modification Privileges Not Assigned To User"},
                            status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(responses=BookSerializer)
    @transaction.atomic()
    def delete(self, request, book_id):
        book = Book.objects.get(id=book_id)

        if book.user == request.user:
            book.delete()

            return Response({"message": "Book Deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Deletion Privileges Not Assigned To User"},
                            status=status.HTTP_401_UNAUTHORIZED)
