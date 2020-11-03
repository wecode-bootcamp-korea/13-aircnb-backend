from django.db import models

# Create your models here.
class Users(models.Model) :
	username			= models.CharField(max_length = 20)
	sex					= models.CharField(max_length = 10)
	email				= models.CharField(max_length = 50)
	phonenumber			= models.CharField(max_length = 14)
	emergency_contact	= models.CharField(max_length = 14)
	introduction		= models.CharField(max_length = 300)
	image_url			= models.CharField(max_length = 2000)
	address				= models.CharField(max_length = 100)
	dob					= models.DateField(auto_now = False, auto_now_add = False)
	password			= models.CharField(max_length = 500)


class Hosts(models.Model) :
	user 		 = models.OneToOneField('Users', on_delete = models.CASCADE)
	stay 		 = models.ForeignKey('Stays', on_delete = models.CASCADE)
	is_verified  = models.BooleanField()
	is_superhost = models.BooleanField()
