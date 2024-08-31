from django.db import models
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.item import Item


class ItemCategory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'category')