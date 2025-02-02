from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from ..serializers import QuotationSerializer
from rest_framework import status
from ..models import Quotation


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def quotation_handler(request, pk=None):
    user = request.user
    if request.method == 'POST':
        serializer = QuotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Quotation created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method =="GET":
        if pk:
            try:
                quotation = Quotation.objects.get(pk=pk, user=user)
                serializer = QuotationSerializer(quotation),
                return Response({"message": "Quotation retrieved successfully", 'data': serializer.data}, status=status.HTTP_200_OK)
            except Quotation.DoesNotExist:
                return Response({"error": "Quotation not found"}, status=status.HTTP_404_NOT_FOUND)

        quotations = Quotation.objects.filter(user=user)
        serializer = QuotationSerializer(quotations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

