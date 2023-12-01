import logging
from sys import stdout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
                    level = logging.DEBUG,
                    format= LOG_FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger:logging.Logger = logging.getLogger()


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


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        

        user = CustomUser.objects.filter(username=username).first()


        logger.info({})
        logger.info({user.password})


        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            response_data = {'token': token.key}
            serializer = UserSerializer(instance=user)
            response_data.update(serializer.data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
