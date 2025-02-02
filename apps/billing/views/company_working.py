from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import CompanyWorkingSerializer
from ..models import Company, Working
from rest_framework import status


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_working_handler(request, pk=None):
    user = request.user

    if request.method == 'POST':
        company_id = request.data.get('company')
        if not company_id:
            return Response({"error": "Company id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(id=company_id, user=user)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found or does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyWorkingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        company_id = request.query_params.get("company", None)
        if pk:
            try:
                working = Working.objects.get(pk=pk, user=user)
                serializer = CompanyWorkingSerializer(working)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Working.DoesNotExist:
                return Response({"error": "Working not fount"}, status=status.HTTP_404_NOT_FOUND)
        workings = Working.objects.filter(user=user)
        if company_id:
            workings = workings.filter(company=company_id)
        serializer = CompanyWorkingSerializer(workings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not pk:
            return Response({"error": "Working id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            working = Working.objects.get(pk=pk, user=user)
        except Working.DoesNotExist:
            return Response({"error": "Working  not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyWorkingSerializer(working, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not pk:
            return Response({"error": "working id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            working = Working.objects.get(pk=pk, user=user)
        except Working.DoesNotExist:
            return Response({"error": "working not found"}, status=status.HTTP_404_NOT_FOUND)
        working.delete()
        return Response({"message": "Company working deleted successfully"}, status=status.HTTP_205_RESET_CONTENT)


