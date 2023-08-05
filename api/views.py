from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import BookListSerializer, BookDetailSerializer, BookPartialSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from backend.models import Book

class BookViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
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

    def create(self, request):
        request.data['user'] = request.user.id
        serializer = BookDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Book created", status=200)

    def update(self, request, pk=None):
        queryset = Book.objects.filter(user=request.user)
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookDetailSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Book edited successfully", status=200)

    def partial_update(self, request, pk=None):
        queryset = Book.objects.filter(user=request.user)
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookPartialSerializer(instance=book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Book edited successfully", status=200)
    
    def destroy(self, request, pk=None):
        queryset = Book.objects.filter(user=request.user)
        book = get_object_or_404(queryset, pk=pk)
        book.delete()
        return Response("Book deleted", status=202)