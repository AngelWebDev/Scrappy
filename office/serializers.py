from rest_framework import serializers
from .models import ScrappyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappyUser
        fields = ['id', 'email', 'firstname', 'lastname', 'status']
