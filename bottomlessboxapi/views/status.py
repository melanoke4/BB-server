from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from bottomlessboxapi.models.status import Status

class StatusViewSet(viewsets.ViewSet):

    def list(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        status_obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status_obj)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        status_obj = get_object_or_404(Status, pk=pk)
        status_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']
