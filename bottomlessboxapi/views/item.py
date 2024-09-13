from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.item import Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from bottomlessboxapi.models.lore import Lore
from bottomlessboxapi.models.review import Review
from bottomlessboxapi.models.user import User
from bottomlessboxapi.views.lore import LoreSerializer
from bottomlessboxapi.views.review import ReviewSerializer



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
            item = get_object_or_404(Item, pk=pk, user=request.query_params.get('user_id'))
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
    lore = LoreSerializer(required=False, allow_null=True)
    review = ReviewSerializer(required=False, allow_null=True)

    class Meta:
        model = Item
        fields = ['id', 'user', 'name', 'cost', 'purchase_date', 'categories', 'category_names',
                  'location', 'location_name', 'status', 'status_name', 'image_url', 'lore', 'review']
        read_only_fields = ['id', 'user']

    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        lore_data = validated_data.pop('lore', None)
        review_data = validated_data.pop('review', None)
        
        item = Item.objects.create(**validated_data)
        item.categories.set(categories)
        
        if lore_data:
            Lore.objects.create(item=item, **lore_data)
        
        if review_data:
            Review.objects.create(item=item, **review_data)
        
        # Refresh the item instance to include the newly created lore and review
        item.refresh_from_db()
        return item

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'lore') and instance.lore:
            representation['lore'] = LoreSerializer(instance.lore).data
        if hasattr(instance, 'review') and instance.review:
            representation['review'] = ReviewSerializer(instance.review).data
        return representation

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        lore_data = validated_data.pop('lore', None)
        review_data = validated_data.pop('review', None)
        
        instance = super().update(instance, validated_data)
        
        if categories is not None:
            instance.categories.set(categories)
        
        if lore_data:
            if instance.lore:
                for attr, value in lore_data.items():
                    setattr(instance.lore, attr, value)
                instance.lore.save()
            else:
                lore = Lore.objects.create(**lore_data)
                instance.lore = lore
        
        if review_data:
            if instance.review:
                for attr, value in review_data.items():
                    setattr(instance.review, attr, value)
                instance.review.save()
            else:
                review = Review.objects.create(**review_data)
                instance.review = review
        
        instance.save()
        return instance