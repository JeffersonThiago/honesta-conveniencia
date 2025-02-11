from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['id', 'is_active']

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