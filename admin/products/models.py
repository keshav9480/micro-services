from django.db import models

# Create your models here.
'''
models are used to create tables in mysql database.
After models are created, need to migrate the models such that informing django that developer will make use of this models
reference: https://docs.djangoproject.com/en/3.2/topics/db/models/
'''

class Product(models.Model):

    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

