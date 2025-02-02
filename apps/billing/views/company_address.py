from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import CompanyAddressSerializer
from ..models import Company, CompanyAddress


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_address_handler(request, pk=None):
    user = request.user
    if request.method == 'POST':
        company_id = request.data.get('company')
        if not company_id:
            return Response({"error": "company id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(id=company_id, user=user)
        except Company.DoesNotExist:
            return Response({"error": "Company not found or owned by user"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CompanyAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        company_id = request.query_params.get("company", None)
        if pk:
            try:
                address = CompanyAddress.objects.get(pk=pk, user=user)
                serializer = CompanyAddressSerializer(address)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CompanyAddress.DoesNotExist:
                return Response({"error": "Company address not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            addresses = CompanyAddress.objects.filter(user=user)
            if company_id:
                addresses = addresses.filter(company=company_id)
            serializer = CompanyAddressSerializer(addresses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not pk:
            return Response({'error': "address id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            address = CompanyAddress.objects.get(pk=pk, user=user)
        except CompanyAddress.DoesNotExist:
            return Response({'error': "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyAddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if not pk:
            return Response({"error": "address id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            address = CompanyAddress.objects.get(pk=pk, user=user)
        except CompanyAddress.DoesNotExist:
            return Response({"error": "address not found"}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "address deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)






