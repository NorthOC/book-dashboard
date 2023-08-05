from django.urls import path
from .views import LoginView, RegisterView, DashboardView
from .views import LogoutView, DeleteView, EditView, DetailView
from .views import CreateView, PatchView

app_name = 'frontend'

urlpatterns = [
    path("", LoginView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("books/", DashboardView.as_view(), name="dashboard"),
    path("book/<str:id>/", DetailView.as_view(), name="details" ),
    path("dashboard/create/", CreateView.as_view(), name="create"),
    path("delete/book/<str:id>/", DeleteView.as_view(), name="delete"),
    path("edit/book/<str:id>/", EditView.as_view(), name="update"),
    path("quick-edit/book/<str:id>/", PatchView.as_view(), name="patch"),
]