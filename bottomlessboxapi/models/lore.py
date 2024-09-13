from django.db import models
from bottomlessboxapi.models.item import Item

class Lore(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='lore')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)