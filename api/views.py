from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import UserSerializer, BookListSerializer, BookDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from backend.models import Book, User
import datetime, jwt
from core.settings import SECRET_KEY

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("jwt expired")
        
        user = User.objects.get(id=payload['id'])

        serializer = UserSerializer(instance=user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response
    
class BookViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Book.objects.filter(user=request.user)
        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.filter(user=request.user)
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)