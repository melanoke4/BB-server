
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from bottomlessboxapi.models.item import Item
from bottomlessboxapi.models.review import Review


class ReviewViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     """
    #     This view should return a list of all reviews
    #     for items owned by the currently authenticated user.
    #     """
    #     return Review.objects.filter(item__user=self.request.user)

    def create(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Update a review instance.
        Ensure the associated item belongs to the current user.
        """
        instance = self.get_object()
        if instance.item.user != request.user:
            return Response({"detail": "You do not have permission to edit this review."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a review instance.
        Ensure the associated item belongs to the current user.
        """
        instance = self.get_object()
        if instance.item.user != request.user:
            return Response({"detail": "You do not have permission to delete this review."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

# The ReviewSerializer remains the same
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'item', 'content', 'created_at']
        read_only_fields = ['created_at']

    # def validate_item(self, value):
    #     if value.user != self.context['request'].user:
    #         raise serializers.ValidationError("You can only review your own items.")
    #     return value