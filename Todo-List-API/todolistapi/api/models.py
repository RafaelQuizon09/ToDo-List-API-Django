from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Users(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username is still required but not used for authentication


class Todos(models.Model):
    todoID = models.AutoField(primary_key=True)
    todoTitle = models.CharField(max_length=100)
    todoDescription = models.CharField(max_length=10000)
    todoStatus = models.CharField(max_length=100)
    dueDate = models.DateField()
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    def __str__ (self):
        return self.todoTitle