from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Обязательно используем set_password
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ChatSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Chat, используется для создания и получения информации о чатах.
    """
    class Meta:
        model = Chat
        fields = ['id', 'user', 'manager', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Message, используется для создания и получения сообщений.
    """
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'text', 'timestamp']
        read_only_fields = ['timestamp']
