from django.db import models
from bottomlessboxapi.models.category import Category
from bottomlessboxapi.models.location import Location
from bottomlessboxapi.models.status import Status
from bottomlessboxapi.models.user import User

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    image_url = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='items')