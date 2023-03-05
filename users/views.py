
# Django REST Framework

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import permissions
from users.serializers import UserSignUpSerializer,  \
    UserModelSerializer, ChangePasswordSerializer
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.middleware import csrf
from django.urls import reverse_lazy
import jwt
from django.conf import settings

# Models
from users.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwars):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                print(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
                response.set_cookie(
                    key='xisto_access',
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.set_cookie(
                    key='xisto_refresh',
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}
                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


def refresh_get(request):
    try:
        refresh_token = request.COOKIES["xisto_refresh"]
        print('ok')
        return JsonResponse({"refresh": refresh_token}, safe=False)
    except Exception as e:
        print(e)
        return None


class TokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except jwt.ExpiredSignatureError as e:
            raise jwt.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        res.delete_cookie("kodea_access")
        res.set_cookie(
            key='xisto_access',
            value=serializer.validated_data["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        return res


class Logout(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie('xisto_access')
        response.data = {"Success": "Logout"}

        return response


class Signup(GenericAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """User sign up."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserModelSerializer(user).data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse_lazy('users:email-verify')
        print(relative_link)
        absurl = 'http://'+current_site + \
            relative_link + "?token=" + str(token)
        email_body = 'Hola,'+user.username + \
            ' User link bellow to verify your email \n ' + absurl
        data = {'email_body': email_body,
                'to_email': user.email, 'subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)



class VerifyEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            print(user.is_verified)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activaction Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["contraseña erronea"]},
                                status=status.HTTP_400_BAD_REQUEST)
            new_password = serializer.data.get("new_password")
            if old_password == new_password:
                return Response({"Error": ["La contraseña nueva no puede ser igual a la antigua "]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(new_password)
            self.object.save()
            return Response({'succes': "cambio de contraseña realizado con exito"}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
