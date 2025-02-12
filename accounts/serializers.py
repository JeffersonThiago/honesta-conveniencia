from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['id', 'is_active', 'user']

    def validate(self, data):        
        password = data.get("password")
        password2 = data.get("password2")
        
        if password != password2:
            raise ValidationError({'msg': 'As senhas informadas não são iguais.'})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError({'msg': 'Usuário já cadastrado com este email.'})
        return value
    

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            email=validated_data.pop('email'),
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name'),
            password=password
        )

        Profile.objects.create(user=user, **validated_data)
        return user