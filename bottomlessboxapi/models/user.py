from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    uid = models.CharField(max_length=50, unique=True)
    

    def __str__(self):
        return self.username