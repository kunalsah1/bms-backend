from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['POST'])
def verify_token(request):
    token = request.data.get("token")
    try:
        decoded_token = AccessToken(token)  # Decode JWT
        user_id = decoded_token['user_id']
        return Response({"user": {"id": user_id}}, status=200)
    except Exception:
        return Response({"error": "Invalid Token"}, status=401)
