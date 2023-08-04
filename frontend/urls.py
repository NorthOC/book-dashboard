from django.urls import path
from .views import LoginView, RegisterView, DashboardView, LogoutView, DeleteView, EditView

app_name = 'frontend'

urlpatterns = [
    path("", LoginView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("delete/book/<str:id>/", DeleteView.as_view(), name="delete"),
    path("edit/book/<str:id>/", EditView.as_view(), name="update"),
]