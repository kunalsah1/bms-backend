from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from ..models import Quotation

class DashboardHandler(APIView):
    def get(self, request):
        bill_count = Quotation.objects.filter(bill_or_quotation='bill').count()
        quotation_count = Quotation.objects.filter(bill_or_quotation='quotation').count()

        data = {
            'bill_count': bill_count,
            'quotation_count': quotation_count
        }

        return Response(data)