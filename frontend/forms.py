from backend.models import User, Book
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['user', 'cover']

        widgets = {
            'pubdate': DateInput(),
        }

class BookPatchForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']