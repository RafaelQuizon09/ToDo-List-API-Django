from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Todos
from .serializer import UserSerializer
from .serializer import TodosSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
# Create your views here.

@api_view(['GET'])
def getUser (request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTodo(request):
    user_id = request.query_params.get('userID', None)  # Get userID from query parameters
    if user_id is not None:
        todo = Todos.objects.filter(userID=user_id)  # Filter todos by userID
    else:
        todo = Todos.objects.all()  # Return all todos if no userID is provided
    serializer = TodosSerializer(todo, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    data = request.data
    data['password'] = make_password(data['password'])  # Hash the password before saving
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request=request, email=email, password=password)
    
    if user and user.is_active:
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createTodo(request):
    data = request.data
    serializer = TodosSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateTodo(request):
    data = request.data
    todo_id = data.get('todoID')
    try:
        todo = Todos.objects.get(todoID=todo_id)
    except Todos.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TodosSerializer(todo, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteTodo(request, todo_id):
    try:
        todo = Todos.objects.get(todoID=todo_id)
    except Todos.DoesNotExist:
        return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

    todo.delete()
    return Response({"message": "Todo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def deleteUser(request, user_id):
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)