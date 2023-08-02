from django.shortcuts import render
from rest_framework.views import View

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")