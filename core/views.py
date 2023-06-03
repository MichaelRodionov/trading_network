from typing import Any

from django.contrib.auth import authenticate, login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer


# ----------------------------------------------------------------
# user views
@extend_schema(tags=['User'])
class UserCreateView(CreateAPIView):
    """
    View to handle registration

    Attrs:
        - queryset: defines queryset for this APIView
        - serializer_class: defines serializer class for this APIView
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        description="Create new user instance",
        summary="Registrate user",
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['User'])
class UserLoginView(CreateAPIView):
    """
    View to handle user authentication
    """
    @extend_schema(
        description="Give permissions to user",
        summary="Authenticate user",
    )
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Method to redefine post logic

        Params:
            - request: HttpRequest
            - args: positional arguments
            - kwargs: named (keyword) arguments

        Returns:
            - Response: Successful login

        Raises:
            - AuthenticationFailed (in case of invalid username or password)
        """
        user: Any = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
            return Response('Successful login', status=status.HTTP_200_OK)
        raise AuthenticationFailed('Invalid username or password')
