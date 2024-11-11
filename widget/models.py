from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    telegram_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Настройки related_name для избежания конфликтов
    groups = models.ManyToManyField(
        Group,
        related_name='widget_user_groups',  # Уникальное имя связи
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='widget_user_permissions',  # Уникальное имя связи
        blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'email'  # Устанавливаем email в качестве идентификатора
    REQUIRED_FIELDS = ['username']  # Обязательные поля при создании суперпользователя

    def __str__(self):
        return self.username



class Manager(models.Model):
    """
    Модель менеджера, представляющая сотрудника, который может общаться с пользователями через чат.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Поле, указывающее, активен ли менеджер.

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    """
    Модель чата, представляющая чат-сессию между пользователем и менеджером.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat with {self.user.username}"


class Message(models.Model):
    """
    Модель сообщений, представляющая сообщения в рамках определенного чата.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
