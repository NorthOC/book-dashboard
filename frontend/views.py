from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, BookForm, BookPatchForm
from django.views.generic import TemplateView
from backend.services import user_token_service, authenticate_service
from backend.services import book_list_service, book_detail_service
from backend.services import book_delete_service, book_create_service
from backend.services import book_edit_service, book_patch_service
from django.contrib.auth.models import Permission

class LoginView(TemplateView):

    def get(self, request):
        access_token = request.COOKIES.get("access")

        if access_token is not None and (authenticate_service(request)):
            return redirect("frontend:dashboard")
        
        response = render(request, "login.html")
        response.delete_cookie("access")

        return response
    
    def post(self, request):
        token_payload = user_token_service(request)
        status_code = token_payload['status_code']
        data = token_payload['body']

        if status_code == 200:
            response = redirect('frontend:dashboard')
            response.set_cookie(key="access", value=data['access'], samesite="Lax")
        elif status_code == 401:
            response = render(request, "login.html")
            messages.add_message(request, messages.ERROR, "Invalid username or passwords. Please try again.")
        else:
            messages.add_message(request, messages.ERROR, "Oops! One of of your fields was left empty! Please try again.")
            response = render(request, "login.html")

        return response

class LogoutView(TemplateView):
    def get(self, request):
        response = redirect('frontend:index')
        response.delete_cookie("access")
        return response

class RegisterView(TemplateView):
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
            c_book_perm = Permission.objects.get(codename="add_book")
            r_book_perm = Permission.objects.get(codename="view_book")
            u_book_perm = Permission.objects.get(codename="change_book")
            d_book_perm = Permission.objects.get(codename="delete_book")
            permissions = [c_book_perm, r_book_perm, u_book_perm, d_book_perm]
            user.save()
            user.user_permissions.set(permissions)
            return redirect("frontend:index")
        
        messages.add_message(request, messages.ERROR, "There was a problem creating your account. Make sure that you follow field requirements.")
        return render(request, "register.html")

class DashboardView(TemplateView):

    def get(self, request):
        token = request.COOKIES.get("access")
        if token is None or not authenticate_service(request):
                return redirect("frontend:index")

        book_list_payload = book_list_service(request)
        status_code = book_list_payload['status_code']
        data = book_list_payload['body']


        if status_code == 200:

            page_number = request.GET.get('page_number') 
            if page_number != None or page_number != "":
                try:
                    page_number = int(page_number)
                except:
                    page_number = 1

            items_per_page = request.GET.get('items_per_page') 
            if items_per_page == None or items_per_page == "":
                try:
                    items_per_page = int(items_per_page)
                except:
                    items_per_page = 3

            # get params from pagination urls
            if data['next'] is not None:
                data['next'] = data['next'].split('/')[-1].split("=")[-1]
            
            if data['previous'] is not None:
                data['previous'] = data['previous'].split('/')[-1].split("=")[-1]

            context = {'books': data['results'],
                       'next_url_params': data['next'],
                       'prev_url_params': data['previous'],
                       'current_page': page_number,
                       'items_per_page': items_per_page,
                       'total_pages': data['count']}
            
            return render(request, "dashboard.html", context)
        return redirect("frontend:index")
    
class DetailView(TemplateView):
    def get(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
            return redirect("frontend:index")    
        
        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 200:
            context = {'book': data}
            return render(request, "book-details.html", context) 
        else:
            return render(request, '404.html')
    
class DeleteView(TemplateView):
    def get(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")
        
        delete_payload = book_delete_service(request, id)
        status_code = delete_payload['status_code']
        data = delete_payload['body']

        if status_code == 202:
            return redirect("frontend:dashboard")
        elif status_code == 404:
            return render(request, '404.html')
        else:
            messages.add_message(request, messages.ERROR, data)
            return render(request, "delete-error.html")
        
class EditView(TemplateView):
    def get(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")

        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 200:
            form = BookForm(data=data)
            context = {'form': form}
            return render(request, "edit.html", context) 
        else:
            return render(request, '404.html')
    
    def post(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
            return redirect("frontend:index")
        create_payload = book_edit_service(request, id)
        status_code = create_payload['status_code']
        data = create_payload['body']
        
        if status_code == 200:
            return redirect("frontend:dashboard")
        else:
            form = BookForm(data=request.POST)
            context = {'form': form}
            for key, err in data.items():
                messages.add_message(request, messages.ERROR, f"{key} - {err[0]}")
            return render(request, "edit.html", context)

class CreateView(TemplateView):
    def get(self, request):  
        if request.COOKIES.get("access") is None or not authenticate_service(request):
            return redirect("frontend:index")
        
        form = BookForm()
        context = {'form': form}
        return render(request, 'create.html', context)
    
    def post(self, request):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
            return redirect("frontend:index")
        
        create_payload = book_create_service(request)
        status_code = create_payload['status_code']
        data = create_payload['body']
        
        if status_code == 200:
            return redirect("frontend:dashboard")
        else:
            form = BookForm(data=request.POST)
            context = {'form': form}
            for key, err in data.items():
                messages.add_message(request, messages.ERROR, f"{key} - {err[0]}")
            return render(request, "create.html", context)
        
class PatchView(TemplateView):
    def get(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
                return redirect("frontend:index")

        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 200:
            form = BookPatchForm(data=data)
            context = {'form': form}
            return render(request, "edit.html", context) 
        else:
            return render(request, '404.html')
    
    def post(self, request, id):
        if request.COOKIES.get("access") is None or not authenticate_service(request):
            return redirect("frontend:index")
        create_payload = book_patch_service(request, id)
        status_code = create_payload['status_code']
        data = create_payload['body']
        
        if status_code == 200:
            return redirect("frontend:dashboard")
        else:
            form = BookForm(data=request.POST)
            context = {'form': form}
            for key, err in data.items():
                messages.add_message(request, messages.ERROR, f"{key} - {err[0]}")
            return render(request, "edit.html", context)