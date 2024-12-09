from django.db import models


class CareerModel(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    created_datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
