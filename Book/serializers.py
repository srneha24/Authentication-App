from rest_framework.serializers import ModelSerializer

from .models import Book


class BookSerializer(ModelSerializer):
    __user_id = None

    class Meta:
        model = Book
        fields = ('book_name', 'writer')

    def set_user(self, user):
        self.__user = user

    def create(self, validated_data):
        validated_data["user"] = self.__user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["user"] = self.__user
        return super().update(instance, validated_data)
