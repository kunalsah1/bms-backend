from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers.company import CompanySerializer
from ..models.comapny import Company
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_handler(request, pk=None):

    user = request.user

    if request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        if pk:
            try:
                company = Company.objects.get(pk=pk, user=user)
                serializer = CompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Company.DoesnotExist:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            companies = Company.objects.filter(user=user)
            serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if not pk:
            return Response({"error": "Company id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(pk=pk, user=user)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not pk:
            return Response({"error": "Company id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(pk=pk, user=user)
        except Company.DoesNotExist:
            return Response({"Company not found"}, status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response({"message": "Company deleted successfully "}, status=status.HTTP_205_RESET_CONTENT)





