from backend.models import User, Book
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['user']

class BookPatchForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']