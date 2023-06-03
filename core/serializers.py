from typing import Any, Type

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


# ----------------------------------------------------------------
# user serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer

    Attrs:
        - password: current user's password
        - password_repeat: repeat of current password
    """
    password = serializers.CharField(
        required=True,
        write_only=True
    )
    password_repeat = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs) -> Any:
        """
        Redefined method to validate incoming data

        Params:
            - validated_data: dictionary with validated data of Board entity

        Returns:
            - attrs: dictionary with data

        Raises:
            - ValidationError (in case of password repeat is wrong)
        """
        if attrs.get('password') != attrs.pop('password_repeat'):
            raise serializers.ValidationError('Password mismatch')
        validate_password(attrs.get('password'))
        return attrs

    def create(self, validated_data) -> Any:
        """
        Redefined create method

        Params:
            - validated_data: dictionary with validated data of User entity

        Returns:
            - user: user object
        """
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model: Type[User] = User
        fields: tuple = ('username', 'password_repeat', 'password')
