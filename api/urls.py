from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    #TokenRefreshView,
    TokenVerifyView
)
from .views import BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='login'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls