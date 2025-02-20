from rest_framework import serializers
from .models import Users, Todos

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()