from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from ..serializers import UnitSerializer
from ..models import Unit


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def unit_handler(request, pk=None):
    user = request.user
    if request.method == "POST":
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if pk:
            try:
                unit = Unit.objects.get(pk=pk, user=user)
                serializer = UnitSerializer(unit)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Unit.DoesNotExist():
                return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            units = Unit.objects.filter(user=user)
            serializer = UnitSerializer(units, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        if not pk:
            return Response({"error": "unit id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            unit = Unit.objects.get(pk=pk, user=user)
        except Unit.DoesNotExist:
            return Response({"error": "unit not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



