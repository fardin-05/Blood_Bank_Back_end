from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import CustomUser

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "age",
            "address",
            "last_donation",
            "availability"
        ]

        
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "age",
            "blood_group",
            "availability",
            "password",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'age',
            'blood_group',
            'availability',
            'last_donation',
            'is_active',
        ]
        read_only_fields = ['id','is_active']

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "address",
            "blood_group",
            "availability"
        ]