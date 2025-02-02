from rest_framework import serializers
from ..models import Quotation


class QuotationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company_id.name', read_only=True)
    company_address = serializers.CharField(source='address_id.address', read_only=True)
    company_working = serializers.CharField(source='working_id.title', read_only=True)
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = Quotation
        fields = "__all__"

