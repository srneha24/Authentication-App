from .models import CustomUser

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'designation')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            designation=validated_data['designation']
        )
        return user
