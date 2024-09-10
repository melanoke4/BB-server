from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from bottomlessboxapi.models.user import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class UserView(ViewSet):

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.username = request.data["username"]
        user.email = request.data["email"]
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request):
        users = User.objects.all()
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "uid")
