from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from bottomlessboxapi.models.category import Category


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('name', '')
        categories = Category.objects.filter(name__icontains=query)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
