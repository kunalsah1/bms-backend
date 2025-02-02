from django.db import models
from ..models import Company, CompanyAddress, Working
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Quotation(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    address_id = models.ForeignKey(CompanyAddress, on_delete=models.CASCADE)
    working_id = models.ForeignKey(Working, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quotation_date = models.DateField()
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    email_id = models.EmailField(max_length=50, null=True, blank=True)
    client_name = models.CharField(max_length=500)
    client_address1 = models.CharField(max_length=500)
    client_address2 = models.CharField(max_length=500)
    total_materials = models.CharField(max_length=20, null=True, blank=True)
    total_labour = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.CharField(max_length=20, null=True, blank=True)
    BILL_OR_QUOTATION_CHOICES = [
        ('bill', 'BILL'),
        ('quotation', 'QUOTATION')
    ]
    bill_or_quotation = models.CharField(max_length=20, choices=BILL_OR_QUOTATION_CHOICES, default='BILL')

    materials = models.JSONField(
        default=list,
    )

    def clean(self):
        super().clean()
        if not isinstance(self.materials, list):
            raise ValidationError("Materials must be an array")
        for item in self.materials:
            if not isinstance(item, dict):
                raise ValidationError("Each entry should be an object")

            required_keys = {"particular", "rate", "quantity", "unit", "amount"}
            item_keys = set(item.keys())
            missing_keys = required_keys - item_keys
            if missing_keys:
                raise ValidationError(f"Missing keys in object: {missing_keys}")
            extra_keys = item_keys - required_keys
            if extra_keys:
                raise ValidationError(f"Extra keys in object are not allowed: {extra_keys}")

            if not isinstance(item['particular'], str):
                raise ValidationError("Particular must be a string")
            if not isinstance(item['rate'], (int, float)):
                raise ValidationError("rate must be a number")
            if not isinstance(item['quantity'], (int, float)):
                raise ValidationError('quantity must be a number')
            if not isinstance(item['amount'], (int, float)):
                raise ValidationError("amount must be a number")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
