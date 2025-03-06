from rest_framework import serializers

class DashboardSerializer(serializers.ModelSerializer):
    bill_count = serializers.IntegerField()
    quotation_count = serializers.IntegerField()
    total_bill_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_Quotation_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
