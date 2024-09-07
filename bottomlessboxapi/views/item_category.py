from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from bottomlessboxapi.models.item_category import ItemCategory
from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.category import Category
from rest_framework import serializers
from bottomlessboxapi.models.item_category import ItemCategory
from bottomlessboxapi.models.user import User

class ItemCategoryViewSet(viewsets.ViewSet):
    
    def list(self, request):
        """List all ItemCategories for the current user"""
        item_categories = ItemCategory.objects.filter(item__user=request.user)
        serializer = ItemCategorySerializer(item_categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new ItemCategory"""
        item_id = request.data.get('item')
        category_id = request.data.get('category')

        # Ensure the item belongs to the current user
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        item = get_object_or_404(Item, id=item_id, user=user)
        category = get_object_or_404(Category, id=category_id)

        # Check if the association already exists
        if ItemCategory.objects.filter(item=item, category=category).exists():
            return Response(
                {"detail": "This item is already associated with this category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        item_category = ItemCategory.objects.create(item=item, category=category)
        serializer = ItemCategorySerializer(item_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Retrieve a specific ItemCategory"""
        item_category = get_object_or_404(ItemCategory, pk=pk, item__user=request.user)
        serializer = ItemCategorySerializer(item_category)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update an ItemCategory"""
        item_category = get_object_or_404(ItemCategory, pk=pk, item__user=request.user)
        
        item_id = request.data.get('item')
        category_id = request.data.get('category')

        # Ensure the new item (if changed) belongs to the current user
        if item_id:
            item = get_object_or_404(Item, id=item_id, user=request.user)
            item_category.item = item
        
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            item_category.category = category

        item_category.save()
        serializer = ItemCategorySerializer(item_category)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """Partially update an ItemCategory"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Delete an ItemCategory"""
        item_category = get_object_or_404(ItemCategory, pk=pk, item__user=request.user)
        item_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple ItemCategories at once"""
        item_id = request.data.get('item')
        category_ids = request.data.get('categories', [])

        item = get_object_or_404(Item, id=item_id, user=request.user)
        
        created_item_categories = []
        for category_id in category_ids:
            category = get_object_or_404(Category, id=category_id)
            item_category, created = ItemCategory.objects.get_or_create(item=item, category=category)
            if created:
                created_item_categories.append(item_category)

        serializer = ItemCategorySerializer(created_item_categories, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'item', 'category']