from django.db import models

# Create your models here.
class Booking(models.Model) :
	stay 		 = models.ForeignKey('Stays', on_delete = models.CASCADE)
	user 		 = models.ForeignKey('Users', on_delete = models.CASCADE)
	checkin_date = models.DateField(auto_now=False, auto_now_add=False)
	checkout_date= models.DateField(auto_now=False, auto_now_add=False)
	guests 		 = models.IntegerField()
	price 		 = models.DecimalField(max_digits=1000, decimal_places=2)
	creditcard 	 = models.CharField(max_length=200)
	request_date = models.DateField(auto_now=False, auto_now_add=False)
	accept_date  = models.DateField(auto_now=False, auto_now_add=False)


class Cancellation(models.Model) :
	booking 	= models.ForeignKey('Booking', on_delete = models.CASCADE)
	user 		= models.ForeignKey('Users', on_delete = models.CASCADE)
	cancel_date = models.DateField(auto_now=False, auto_now_add=False)