from importlib.resources import contents
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serialiser import UserSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import MyUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserAll(APIView):
    """
    List all Users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        #will use serialiser here 
        all_users = list(MyUser.objects.all().values())
        return Response({"all_users" : all_users})


class UserRegister(APIView):
    """
    UserRegistration view: This will create a user account and will generate the access token.
    This generated access token will be used to access other services
    """
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'Registion success', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class UserLogin(APIView):
    """
    UserRegistration view: This will authenticate user account and will generate the access token.
    This generated access token will be used to access other services
    """
    def post(self, request, format=None):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(email, password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_fields_error': ['Email or password is not valid']}})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
