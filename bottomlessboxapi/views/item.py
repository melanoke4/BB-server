from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.item import Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from bottomlessboxapi.models.user import User



class ItemViewSet(viewsets.ViewSet):

    def list(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            items = Item.objects.filter(user=user)
        else:
            items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(pk=request.data["user_id"])
            except ObjectDoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            item = get_object_or_404(Item, pk=pk, user=request.user)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        item = get_object_or_404(Item, pk=pk, user=user)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        item = get_object_or_404(Item, pk=pk, user=user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    category_names = serializers.SerializerMethodField()
    location_name = serializers.ReadOnlyField(source='location.name')
    status_name = serializers.ReadOnlyField(source='status.name')

    class Meta:
        model = Item
        fields = ['id', 'user', 'name', 'cost', 'purchase_date', 'categories', 'category_names',
                  'location', 'location_name', 'status', 'status_name', 'image_url']
        read_only_fields = ['id', 'user']

    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        item = Item.objects.create(**validated_data)
        item.categories.set(categories)
        return item

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        instance = super().update(instance, validated_data)
        if categories is not None:
            instance.categories.set(categories)
        return instance