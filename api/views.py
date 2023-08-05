from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import BookListSerializer, BookDetailSerializer, BookPartialSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from backend.models import Book
from django.db.models import Q

class BookViewSet(PageNumberPagination, viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    page_size = 3
    page_size_query_param = 'items_per_page'
    max_page_size = 5


    def list(self, request):

        q = request.data.get('q')
        date_from = request.data.get('date_from')
        date_to = request.data.get('date_to')

        if q is None:
            q = ""

        if date_from == "" or date_from is None:
            date_from = '0001-01-01'

        if date_to == "" or date_to is None:
            date_to = '9999-12-31'

        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.filter(          
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(author__icontains=q) |
                Q(user__username__icontains=q) &
                Q(pubdate__lte=date_to) & 
                Q(pubdate__gte=date_from)
                ).order_by("-pubdate")
        elif request.user.has_perm("backend.view_book"):
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
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
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
        if request.user.has_perm("backend.create_book") or request.user.has_perm("backend.administrator"):
            request.data['user'] = request.user.id
            serializer = BookDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Book created", status=200)
        return Response("User is authenticated but does not have proper permission", status=403)

    def update(self, request, pk=None):
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
        if request.user.has_perm("backend.administrator"):
            queryset = Book.objects.all()
        elif request.user.has_perm("backend.delete_book"):
            queryset = Book.objects.filter(user=request.user)
        else:
            return Response("User is authenticated but does not have proper permission", status=403)
        book = get_object_or_404(queryset, pk=pk)
        book.delete()
        return Response("Book deleted", status=202)