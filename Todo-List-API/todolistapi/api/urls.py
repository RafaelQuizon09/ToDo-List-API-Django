from django.urls import path

from .views import getUser, getTodo, loginUser, createUser, createTodo, updateTodo, deleteTodo, deleteUser

urlpatterns = [
    path('getUser/', getUser, name='getUser'),
    path('getTodo/', getTodo, name='getTodo'),
    path('loginUser/', loginUser, name='loginUser'),
    path('createUser/', createUser, name='createUser'),
    path('createTodo/', createTodo, name='createTodo'),
    path('updateTodo/', updateTodo, name='updateTodo'),
    path('deleteTodo/<int:todo_id>/', deleteTodo, name='deleteTodo'),
    path('deleteUser/<int:user_id>/', deleteUser, name='deleteUser'),
]