from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'mobile_number', 'password')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user