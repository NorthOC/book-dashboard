from rest_framework import serializers
from backend.models import User, Book
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validate_password(password=password)
        instance = self.Meta.model(**validated_data)
        c_book_perm = Permission.objects.get(codename="add_book")
        r_book_perm = Permission.objects.get(codename="view_book")
        u_book_perm = Permission.objects.get(codename="change_book")
        d_book_perm = Permission.objects.get(codename="delete_book")
        permissions = [c_book_perm, r_book_perm, u_book_perm, d_book_perm]
        if password is not None:
            instance.set_password(password)
            instance.save()
            instance.user_permissions.set(permissions)
            return instance

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'user']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"