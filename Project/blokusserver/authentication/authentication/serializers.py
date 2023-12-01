# authentication/serializers.py
import logging
from sys import stdout
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.StreamHandler(stdout)],
                    level = logging.DEBUG,
                    format= LOG_FORMAT,
                    datefmt='%d/%m/%Y %H:%M:%S')

logger:logging.Logger = logging.getLogger()


##################################################
## Author: Luis Eckert
##################################################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        logger.info({validated_data['password']})
        validated_data['password'] = make_password(validated_data['password'])
        logger.info({validated_data['password']})
        return super(UserSerializer, self).create(validated_data)
