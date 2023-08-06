from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, BookForm, BookPatchForm
from django.views.generic import TemplateView
from .services import user_token_service, authenticate_service
from .services import book_list_service, book_detail_service
from .services import book_delete_service, book_create_service
from .services import book_edit_service, book_patch_service, get_username_service
from django.contrib.auth.models import Permission
from datetime import datetime

class LoginView(TemplateView):
    def get(self, request):
        auth = authenticate_service(request)

        if auth['status_code'] != 200:
            response = render(request, "login.html")
            response.delete_cookie("access")
            return response
            
        return redirect("frontend:dashboard")
        
    
    def post(self, request):
        token_payload = user_token_service(request)
        status_code = token_payload['status_code']
        data = token_payload['body']

        if status_code == 200:
            response = redirect('frontend:dashboard')
            response.set_cookie(key="access", value=data['access'], samesite="Lax")
        elif status_code == 401:
            messages.add_message(request, messages.ERROR, 
                                 "Invalid username or password. Please try again.")
            response = render(request, "login.html")
        else:
            messages.add_message(request, messages.ERROR, 
                                 "Oops! One of of your fields was left empty! Please try again.")
            response = render(request, "login.html")

        return response

class LogoutView(TemplateView):
    def get(self, request):
        response = redirect('frontend:index')
        response.delete_cookie("access")
        return response

class RegisterView(TemplateView):
    def get(self, request):
        auth = authenticate_service(request)

        if auth['status_code'] != 200:
            context = {'form': UserForm()}
            response = render(request, "register.html", context)
            return response
        
        return redirect("frontend:dashboard")
    
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
        
        messages.add_message(request, messages.ERROR, 
                             "There was a problem creating your account. \
                                Make sure that you follow field requirements.")
        return render(request, "register.html")

class DashboardView(TemplateView):
    def get(self, request):

        book_list_payload = book_list_service(request)
        status_code = book_list_payload['status_code']
        data = book_list_payload['body']

        if status_code != 200:
            return redirect("frontend:index")
        
        username = get_username_service(request)
        if username is None:
            redirect("frontend:index")
        

        page_number = request.GET.get('page_number')
        items_per_page = request.GET.get('items_per_page') 
        q = request.GET.get('q') if request.GET.get('q') != None else ""
        date_from = request.GET.get('date_from') if request.GET.get('date_from') != None else ""
        date_to = request.GET.get('date_to') if request.GET.get('date_to') != None else ""

        if page_number != None or page_number != "":
            try:
                page_number = int(page_number)
            except:
                page_number = 1

        if items_per_page == None or items_per_page == "":
            try:
                items_per_page = int(items_per_page)
            except:
                items_per_page = 3

        context = {'books': data['results'],
                    'next_url_params': data['next'],
                    'prev_url_params': data['previous'],
                    'q': q,
                    'date_from': date_from,
                    'date_to': date_to,
                    'items_per_page': items_per_page,
                    'page_number': page_number,
                    'total_pages': data['count'],
                    'username': username}
        
        return render(request, "dashboard.html", context)

class DetailView(TemplateView):
    def get(self, request, id): 
        
        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 401:
            return redirect("frontend:index")  

        if status_code == 200:
            data['created'] = datetime.strptime(data['created'][:-13], '%Y-%m-%dT%H:%M:%S%f')
            context = {'book': data}
            return render(request, "book-details.html", context) 
        return redirect("frontend:dashboard")
    
class DeleteView(TemplateView):
    def get(self, request, id):
        
        delete_payload = book_delete_service(request, id)
        status_code = delete_payload['status_code']
        data = delete_payload['body']

        if status_code == 401:
            return redirect("frontend:index") 
        
        if status_code == 202:
            return redirect("frontend:dashboard")
        messages.add_message(request, messages.ERROR, data)
        return render(request, "delete-error.html")
        
class EditView(TemplateView):
    def get(self, request, id):

        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 401:
            return redirect("frontend:index") 

        if status_code == 200:
            form = BookForm(data=data)
            context = {'form': form}
            return render(request, "edit.html", context) 
        else:
            return redirect("frontend:dashboard")
    
    def post(self, request, id):
        
        create_payload = book_edit_service(request, id)
        status_code = create_payload['status_code']
        data = create_payload['body']

        if status_code == 401:
            return redirect("frontend:index") 
        
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
        auth = authenticate_service(request)
        if auth['status_code'] != 200:
            return redirect("frontend:index")
        
        form = BookForm()
        context = {'form': form}
        return render(request, 'create.html', context)
    
    def post(self, request):
        
        create_payload = book_create_service(request)
        status_code = create_payload['status_code']
        data = create_payload['body']
        
        if status_code == 401:
            return redirect("frontend:index") 
        
        if status_code == 200:
            return redirect("frontend:dashboard")
        else:
            form = BookForm(data=request.POST)
            context = {'form': form}
            messages.add_message(request, messages.ERROR, data)
            return render(request, "create.html", context)
        
class PatchView(TemplateView):
    def get(self, request, id):

        book_payload = book_detail_service(request, id)
        status_code = book_payload['status_code']
        data = book_payload['body']

        if status_code == 401:
            return redirect("frontend:index") 

        if status_code == 200:
            form = BookPatchForm(data=data)
            context = {'form': form}
            return render(request, "edit.html", context) 
        
        return redirect("frontend:dashboard")
    
    def post(self, request, id):
        create_payload = book_patch_service(request, id)
        status_code = create_payload['status_code']
        data = create_payload['body']

        if status_code == 401:
            return redirect("frontend:index") 
        
        if status_code == 200:
            return redirect("frontend:dashboard")
        else:
            form = BookForm(data=request.POST)
            context = {'form': form}
            for key, err in data.items():
                messages.add_message(request, messages.ERROR, f"{key} - {err[0]}")
            return render(request, "edit.html", context)