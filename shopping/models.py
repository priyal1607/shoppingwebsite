from itertools import count
from django.db.models.deletion import CASCADE
from django.db import models
class category(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
CATEGORY_CHOICES=(
    ('100-200','100-200'),
    ('200-300','200-300'),
    ('300-400','300-400'),
    ('400-500','400-500')
)
class product(models.Model):
    name=models.CharField(max_length=20)
    cat=models.ForeignKey(category,on_delete=CASCADE)
    img=models.ImageField(upload_to='photo')
    description=models.CharField(max_length=400)
    availableproduct=models.IntegerField()
    price=models.IntegerField()
    range=models.CharField(choices=CATEGORY_CHOICES,max_length=500,default='100-200')
    color=models.CharField(default="red",max_length=20)
    size=models.CharField(default='XL',max_length=3)
    date=models.DateField(default="16-02-2002")
    def __str__(self):
        return self.name

class register(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phoneno=models.IntegerField()
    password=models.CharField(max_length=10)
    cpassword=models.CharField(max_length=10)
    def __str__(self) :
        return self.name

class addtocart(models.Model):
    personname=models.ForeignKey(register,on_delete=CASCADE)
    productname=models.ForeignKey(product,on_delete=CASCADE)
    price=models.IntegerField()
    updated=models.DateTimeField(auto_now_add=False,null=True)
    #status=models.IntegerField()
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return self.personname.name

class deresses(models.Model):
    name=models.CharField(max_length=20)
    img=models.ImageField(upload_to='photo')
    def __str__(self):
        return self.name

# Create your models here.
