from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.lore import Lore

class LoreViewSet(viewsets.ViewSet):

    def list(self, request):
        # Optionally filter by item_id if provided in query params
        item_id = request.query_params.get('item_id')
        if item_id:
            lores = Lore.objects.filter(item_id=item_id)
        else:
            lores = Lore.objects.all()
        serializer = LoreSerializer(lores, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LoreSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the user owns the item they're adding lore to
            item = get_object_or_404(Item, pk=serializer.validated_data['item'].id)
            if item.user != request.user:
                return Response({"detail": "You do not have permission to add lore to this item."},
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        lore = get_object_or_404(Lore, pk=pk)
        # Check if the user owns the item associated with this lore
        if lore.item.user != request.user:
            return Response({"detail": "You do not have permission to view this lore."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = LoreSerializer(lore)
        return Response(serializer.data)

    def update(self, request, pk=None):
        lore = get_object_or_404(Lore, pk=pk)
        # Check if the user owns the item associated with this lore
        if lore.item.user != request.user:
            return Response({"detail": "You do not have permission to update this lore."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = LoreSerializer(lore, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        lore = get_object_or_404(Lore, pk=pk)
        # Check if the user owns the item associated with this lore
        if lore.item.user != request.user:
            return Response({"detail": "You do not have permission to delete this lore."},
                            status=status.HTTP_403_FORBIDDEN)
        lore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lore
        fields = ['id', 'item', 'content', 'created_at']
        read_only_fields = ['created_at']

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Lore content must be at least 10 characters long.")
        return value