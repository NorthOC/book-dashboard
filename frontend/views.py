from django.shortcuts import render, redirect
from rest_framework.views import View
from .forms import UserForm
from backend.services import user_token_service, authenticate_service, book_list_service
from django.contrib import messages

class LoginView(View):

    def get(self, request):
        access_token = request.COOKIES.get("access")
        response = render(request, "login.html")

        if access_token is not None and (authenticate_service(request)):
            return redirect("frontend:dashboard")
        else:
            response.delete_cookie("access")

        return response
    
    def post(self, request):
        token_payload = user_token_service(request)
        status_code = token_payload['status_code']
        data = dict(token_payload['body'])

        if status_code == 200:
            response = redirect('frontend:dashboard')
            response.set_cookie(key="access", value=data['access'], samesite="Lax")
        else:
            messages.add_message(request, messages.ERROR, data['detail'])
            response = render(request, "login.html")

        return response

class LogoutView(View):
    def get(self, request):
        response = redirect('frontend:index')
        response.delete_cookie("access")
        return response

class RegisterView(View):
    def get(self, request):
        access_token = request.COOKIES.get("access")
        if access_token is not None:
            if (authenticate_service(request)):
                return redirect("frontend:dashboard")

        context = {
            'form': UserForm()
        }

        response = render(request, "register.html", context)
        
        return response
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect("frontend:index")
        messages.add_message(request, messages.ERROR, "There was a problem creating your account. Make sure that you follow field requirements.")
        return render(request, "register.html")

class DashboardView(View):
    def get(self, request):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")
        
        book_list_payload = book_list_service(request)
        status_code = book_list_payload['status_code']
        data = book_list_payload['body']

        if status_code == 200:
            context = {'books': data}
        return render(request, "dashboard.html", context)
    
class DeleteView(View):
    def get(self,request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")

class EditView(View):
    def get(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")
        