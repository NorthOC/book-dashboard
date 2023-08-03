from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import UserSerializer, BookListSerializer, BookDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework import viewsets
from backend.models import Book

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
        except ValidationError:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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