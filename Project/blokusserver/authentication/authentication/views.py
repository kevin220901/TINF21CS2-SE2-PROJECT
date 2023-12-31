from rest_framework.authtoken.models import Token
import logging
from sys import stdout
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer, UserWithouPwdSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
                    level = logging.DEBUG,
                    format= LOG_FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger:logging.Logger = logging.getLogger()


##################################################
## Author: Luis Eckert
##################################################


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        #Hashing the password before saving the user
        serializer.save(password=serializer.validated_data['password'])


##################################################
## Author: Luis Eckert
##################################################


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        

        user = CustomUser.objects.filter(username=username).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            response_data = {'token': token.key, 'id': user.id, 'username': user.username}
            serializer = UserSerializer(instance=user)
            response_data.update(serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            logger.critical(f'failt authentication for user {username}')
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = UserWithouPwdSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"new_password": ["This field is required."]}, 
                            status=status.HTTP_400_BAD_REQUEST)


        user.set_password(new_password)
        user.save()

        # invalidate Token an create new one
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)

        response_data = {'token': new_token.key, 'id': user.id, 'username': user.username}

        return Response(response_data, status=status.HTTP_200_OK)