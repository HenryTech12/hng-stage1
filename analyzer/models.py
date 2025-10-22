from django.db import models

# Create your models here.
class Analyzer(models.Model):
    id = models.CharField(unique=True,max_length=255,primary_key=True)
    value = models.CharField(unique=True,max_length=255)
    properties = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)