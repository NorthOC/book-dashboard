from rest_framework import serializers
from backend.models import Book

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover', 'user']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BookPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author"]