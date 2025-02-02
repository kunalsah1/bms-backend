from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.user import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)