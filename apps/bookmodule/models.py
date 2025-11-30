from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)   
    year = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    edition = models.IntegerField(default=1)

    
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(null=True)
    rating = models.SmallIntegerField(default=1)

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        on_delete=models.SET_NULL,
        related_name='books'
    )
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    
class Address(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        # يجب أن تعرض اسم الطالب وعمره
        return f"{self.name} (Age: {self.age})"

# apps/bookmodule/models.py

# ... (النماذج السابقة) ...

# Task 2: علاقة Many-to-Many
class Address2(models.Model):
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return self.city

class Student2(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    # هنا العلاقة Many-to-Many
    addresses = models.ManyToManyField(Address2) 

    def __str__(self):
        return self.name
    
# Task 3: Image Upload Model
class StudentImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='students/') # يحتاج مكتبة Pillow

    def __str__(self):
        return self.title