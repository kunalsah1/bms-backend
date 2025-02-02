from django.db import models
from ..models.comapny import Company
from django.contrib.auth import get_user_model

User = get_user_model()


class CompanyAddress(models.Model):
    address = models.CharField(max_length=500)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.address
