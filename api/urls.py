from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    #TokenRefreshView,
    TokenVerifyView
)
from .views import BookViewSet, UserView, LogoutView
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='login-api'),
    path('user/', UserView.as_view(), name='user-api'),
    path('logout/', LogoutView.as_view(), name='logout-api'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls