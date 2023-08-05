from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView
)
from .views import BookViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='login-api'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls