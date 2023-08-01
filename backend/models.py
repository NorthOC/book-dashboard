from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        permissions = [
        ("create_book", "Can create book"),
        ("read_book", " Can read book"),
        ("update_book", "Can update book"),
        ("delete_book", "Can delete book"),
        ("administrator", "Can edit other user submissions")
        ]

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=800)
    author = models.CharField(max_length=200, default="Unknown")
    #cover =