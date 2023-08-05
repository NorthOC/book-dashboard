from rest_framework import serializers
from backend.models import Book

class BookListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username", read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover', 'pubdate', 'username']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BookPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author"]