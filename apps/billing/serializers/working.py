from rest_framework import serializers
from ..models import Working


class CompanyWorkingSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Working
        fields = "__all__"
