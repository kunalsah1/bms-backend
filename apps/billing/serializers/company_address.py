from rest_framework import serializers
from ..models.company_address import CompanyAddress


class CompanyAddressSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = CompanyAddress
        fields = "__all__"
