from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="default_pfp.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	#return the name of the customer on the pannel instead of showing it as customer 1 which is by default by djagno
	def __str__(self):
			return self.name
		
class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name	
	
class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 
	name = models.CharField(max_length=200, null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=200, null=True,choices=CATEGORY)
	description=models.CharField(max_length=2000, null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tag=models.ManyToManyField(Tag,blank=True)

	def __str__(self):
	    return self.name

	
class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
	#customer has one to many relationship with product as customer can order multiple products
	#on contarst product has one to one reltionship with the cutomer
	customer=models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)

	status = models.CharField(max_length=200, null=True, choices=STATUS)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return f'{self.customer}: {self.product}'
