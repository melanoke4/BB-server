from django.db import models
from bottomlessboxapi.models.item import Item

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)