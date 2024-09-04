from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from bottomlessboxapi.models.item import Item
from rest_framework import serializers
from bottomlessboxapi.models.review import Review
from bottomlessboxapi.models.user import User

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'item', 'content', 'created_at']
        read_only_fields = ['created_at']
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


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
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        if instance.item.user != user:
            return Response({"detail": "You do not have permission to edit this review."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a review instance.
        Ensure the associated item belongs to the current user.
        """
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        instance = self.get_object()
        if instance.item.user != user:
            return Response({"detail": "You do not have permission to delete this review."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)





