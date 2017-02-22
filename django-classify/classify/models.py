from django.db import models

# Create your models here.

class URL_LIST(models.Model):
    url = models.CharField(max_length=400)
    pub_date = models.DateTimeField('date published')
    category = models.CharField(max_length = 20,default="None")


