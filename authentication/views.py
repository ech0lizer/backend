import jwt
from datetime import timedelta
from backend import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistedToken

from .serializers import RegisterSerializer, LoginSerializer
from .models import User
from .utils import Util


#   Register new User   #
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data  # Saving user data
        serializer = self.serializer_class(data=user)  # Setting user data into serializer_class
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        # Choice User name for sending email.
        if user_data['first_name'] is None:
            user_name = user.username
        else:
            user_name = user.first_name

        token = RefreshToken.for_user(user).access_token

        abs_url = 'http://localhost:3000/verify-email/?token=' + str(token)  # Absolute URL for verify email

        email_data = {
            'email_subject': 'Welcome to Blog, verify your Email.',
            'user_name': user_name,
            'abs_url': abs_url,
            'email_to': user.email,
            'email_template': 'emails/register_email.html'
        }

        Util.send_html_email(email_data)
        return Response(user_data, status=status.HTTP_201_CREATED)


#   Email Verification  #
class EmailVerifyAPIView(APIView):

    @staticmethod
    def post(request):
        token = request.data['token']
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'message': 'Successfully activated', 'type': 'success'},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message': 'Email is already verified', 'type': 'info'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        except KeyError:
            return Response({'message': 'Token is None', 'type': 'error'})
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Activation expired', 'type': 'warning'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'message': 'Invalid token', 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


def resend_email(token):
    payload = jwt.decode(token, settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    token = RefreshToken.for_user(user).access_token
    abs_url = 'http://localhost:3000/verify-email/?token=' + str(token)  # Absolute URL for verify email

    email_data = {
        'email_subject': 'Welcome to Blog, verify your Email.',
        'user_name': user_name,
        'abs_url': abs_url,
        'email_to': user.email,
        'email_template': 'emails/register_email.html'
    }

    Util.send_html_email(email_data)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserInfoAPIView(APIView):

    @staticmethod
    def get(request):
        token = request.headers['authorization']
        token = token[7:]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if user:
                user_info = {
                    'user': {
                        'uid': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'last_login': user.last_login
                    }
                }
                return Response(user_info, status=status.HTTP_200_OK)
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        return Response('Hello')