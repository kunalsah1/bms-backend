from django.db import models
from ..models import Company
from django.contrib.auth import get_user_model

User = get_user_model()


class Working(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
