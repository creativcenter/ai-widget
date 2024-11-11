import logging
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    
    permission_classes = [AllowAny]  # Разрешаем доступ без аутентификации

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Регистрация успешна"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Вход выполнен успешно"}, status=status.HTTP_200_OK)
            return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChatViewSet(viewsets.ModelViewSet):
    """
    API для создания и получения информации о чатах.
    """
    queryset = Chat.objects.all()  # Добавлено для автоматического определения basename
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Показывать только чаты текущего пользователя
        return Chat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически установить текущего пользователя как владельца чата
        serializer.save(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API для отправки и получения сообщений.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        # Дополнительное логирование
        print("Authorization header:", request.headers.get("Authorization"))
        
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Логика сохранения сообщения
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user_chats = Chat.objects.filter(user=self.request.user)
        print("User Chats:", user_chats)
        messages = Message.objects.filter(chat__in=user_chats)
        print("Messages:", messages)
        return messages

    def perform_create(self, serializer):
        # Автоматически установить текущего пользователя как отправителя сообщения
        serializer.save(sender=self.request.user)