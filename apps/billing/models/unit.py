from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    