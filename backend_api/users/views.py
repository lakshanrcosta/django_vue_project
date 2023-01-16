from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import generate_access_token, JWTAuthentication
from .models import User
from .serializers import UserSerializer


@api_view(["POST"])
def register(request):
    data = request.data
    # @Todo Validate request data

    if data["password"] != data["password_confirm"]:
        raise exceptions.APIException("Passwords did no match!")

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    # Getting user
    user = User.objects.filter(email=email).get()
    if user is None:
        raise exceptions.AuthenticationFailed("Cannot find user for given email address!")

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Incorrect password!")

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "jwt": token
    }

    return response


@api_view(["GET"])
def users(request):
    registered_users = User.objects.all()
    serializer = UserSerializer(registered_users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def logout(_):
    response = Response()
    response.delete_cookie(key="jwt")
    response.data = {
        "message": "Success"
    }
    return response


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        response = serializer.data
        return Response({"data": response})
