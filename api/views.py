from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.shortcuts import get_object_or_404
from backend.models import Book
from .serializers import BookListUserSerializer, BookListAdminSerializer, BookDetailSerializer
from .serializers import BookPartialSerializer

class UsernameView(APIView):
    """Get user data if authenticated"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'username': request.user.username
        })


class BookViewSet(PageNumberPagination, viewsets.ViewSet):
    """Standard Book ViewSet API with CRUD functionality"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 3
    page_size_query_param = 'items_per_page'
    max_page_size = 30


    def list(self, request):
        """GET BOOKS"""

        q = request.data.get('q')
        date_from = request.data.get('date_from')
        date_to = request.data.get('date_to')

        if q is None:
            q = ""

        if date_from == "" or date_from is None:
            date_from = '0001-01-01'

        if date_to == "" or date_to is None:
            date_to = '9999-12-31'

        is_admin = request.user.has_perm("backend.administrator")
        is_user = request.user.has_perm("backend.view_book")

        if is_admin:
            queryset = Book.objects.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(author__icontains=q) |
                Q(user__username__icontains=q) &
                Q(pubdate__lte=date_to) &
                Q(pubdate__gte=date_from)
                ).order_by("-pubdate")
        elif is_user:
            queryset = Book.objects.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(author__icontains=q) &
                    Q(pubdate__lte=date_to) &
                    Q(pubdate__gte=date_from),
                    user=request.user
                    ).order_by("-pubdate")
        else:
            return Response("User is authenticated but does not have proper permission", status=403)

        page = self.paginate_queryset(queryset, request)
        if page is not None:
            if is_admin:
                serializer = BookListAdminSerializer(page, many=True)
            else:
                serializer = BookListUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if is_admin:
            serializer = BookListAdminSerializer(queryset, many=True)
        else:
            serializer = BookListUserSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET BOOK"""
        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.all()
        elif request.user.has_perm("backend.view_book"):
            queryset = Book.objects.filter(user=request.user)
        else:
            return Response("User is authenticated but does not have proper permission", status=403)

        book = get_object_or_404(queryset, pk=pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


    def create(self, request):
        """CREATE BOOK"""
        if request.user.has_perm("backend.add_book") or request.user.has_perm("backend.administrator"):
            request.data['user'] = request.user.id
            serializer = BookDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response("Book created", status=200)
        return Response("User is authenticated but does not have proper permission", status=403)

    def update(self, request, pk=None):
        """UPDATE BOOK"""
        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.all()
        elif request.user.has_perm("backend.change_book"):
            queryset = Book.objects.filter(user=request.user)
        else:
            return Response("User is authenticated but does not have proper permission", status=403)
        
        book = get_object_or_404(queryset, pk=pk)

        serializer = BookDetailSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Book edited successfully", status=200)

    def partial_update(self, request, pk=None):
        """PATCH BOOK"""
        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.all()
        elif request.user.has_perm("backend.change_book"):
            queryset = Book.objects.filter(user=request.user)
        else:
            return Response("User is authenticated but does not have proper permission", status=403)
        
        book = get_object_or_404(queryset, pk=pk)

        serializer = BookPartialSerializer(instance=book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Book edited successfully", status=200)
    
    def destroy(self, request, pk=None):
        """DELETE BOOK"""
        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.all()
        elif request.user.has_perm("backend.delete_book"):
            queryset = Book.objects.filter(user=request.user)
        else:
            return Response("User is authenticated but does not have proper permission", status=403)
        
        book = get_object_or_404(queryset, pk=pk)
        book.delete()

        return Response("Book deleted", status=202)