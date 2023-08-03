from django.shortcuts import render
from rest_framework.views import View

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

class LogoutView(View):
    def get(self, request):
        return render(request, "logout.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")