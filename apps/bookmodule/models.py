from django.db import models

# Create your models here.

class Book (models.Model):
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.FloatField(default = 0.0)
    edition = models.SmallIntegerField(default = 1)

#lab 8 models
class Address(models.Model):
    city = models.CharField(max_length=100) # [cite: 480]

    def __str__(self):
        return self.city

class Student(models.Model):
    name = models.CharField(max_length=100) # [cite: 478]
    age = models.IntegerField() # [cite: 478]
    # Foreign key to table address [cite: 478]
    address = models.ForeignKey(Address, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name