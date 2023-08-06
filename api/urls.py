from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView
)
from .views import BookViewSet, UsernameView
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
    path('user/', UsernameView.as_view()),
]

urlpatterns += router.urls