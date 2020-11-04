from django.db 		import models

from users.models 	import User, Host
from reviews.models import Review


class Stay(models.Model) :
	name 			= models.CharField(max_length = 100)
	price 			= models.DecimalField(max_digits=1000, decimal_places=2)
	monthly_price	= models.DecimalField(max_digits=1000, decimal_places=2, null=True)
	subcategory 	= models.ForeignKey('Subcategories', on_delete = models.CASCADE)
	stay_type		= models.ForeignKey('RentalTypes', on_delete = models.CASCADE)
	host 			= models.ForeignKey('Host', on_delete = models.CASCADE)
	latitude 		= models.IntegerField()
	longitude 		= models.IntegerField()
	description 	= models.CharField(max_length = 2000)
	bathrooms 		= models.IntegerField()
	capacity 		= models.IntegerField()
	country 		= models.CharField(max_length=50)
	province 		= models.CharField(max_length=50)
	city 			= models.CharField(max_length=50)
	address 		= models.CharField(max_length=500)
	zipcode 		= models.IntegerField()
	created 		= models.DateTimeField(auto_now=True, auto_now_add=True)
	check_in 		= models.DateTimeField(auto_now=False, auto_now_add=False)
	check_out 		= models.DateTimeField(auto_now=False, auto_now_add=False)
	facilities 		= models.ManyToManyField('Facility', through='StayFacility', related_name='stay_facility')
	amenities 		= models.ManyToManyField('Amenity', through='StayAmenity', related_name='stay_amenity')

	class Meta:
		db_table= 'stays'

class Image(models.Model) :
	stay 		= models.ForeignKey(Stay, on_delete=models.CASCADE)
	image_url   = models.URLField(max_length=2000)

	class Meta:
		db_table= 'images'

class Facility(models.Model) :
	names	= models.CharField(max_length=50)
	icon_url= URLField(max_length=2000)

	class Meta:
		db_table= 'facilities'

class StayFacility(models.Model) :
	stay 	 = models.ForeignKey(Stay, on_delete=models.CASCADE)
	facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

	class Meta:
		db_table= 'stay_facilities'

class Amenity(models.Model) :
	name 	 = models.CharField(max_length=50)
	icon_url = models.URLField(max_length=2000)

	class Meta:
		db_table= 'Amenities'

class StayAmenity(models.Model) : 
	stay 	= models.ForeignKey(Stay, on_delete=models.CASCADE)
	amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

	class Meta:
		db_table= 'stay_amenities'

class Category(models.Model) :
	name 	= models.CharField(max_length=50)

	class Meta:
		db_table= 'categories'

class Subcategory(models.Model) :
	name 	 = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		db_table= 'subcategories'

class RentalType(models.Model) :
	name 	= models.CharField(max_length=50)
	icon_url= models.URLField(max_length=2000)

	class Meta:
		db_table= 'rental_types'

class HouseRule(models.Model) :
	stay 	= models.ForeignKey(Stay, on_delete=models.CASCADE)
	name 	= models.CharField(max_length=100)
	icon_url= models.URLField(max_length=2000)

	class Meta:
		db_table= 'house_rules'

class Room(models.Model) :
	stay 	= models.ForeignKey(Stay, on_delete=models.CASCADE)
	name 	= models.CharField(max_length=50)
	beds 	= models.IntegerField()

	class Meta:
		db_table= 'rooms'