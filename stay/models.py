from django.db import models

from user.models   import User, Host

class Stay(models.Model) :
    name          = models.CharField(max_length = 100)
    price         = models.DecimalField(max_digits=60, decimal_places=2)
    discount_price= models.DecimalField(max_digits=60, decimal_places=2, null=True)
    subcategory   = models.ForeignKey('Subcategory', on_delete = models.CASCADE)
    stay_type     = models.ForeignKey('RentalType', on_delete = models.CASCADE)
    host          = models.ForeignKey(Host, on_delete = models.CASCADE)
    latitude      = models.DecimalField(max_digits=8, decimal_places=6)
    longitude     = models.DecimalField(max_digits=9, decimal_places=6)
    description   = models.CharField(max_length = 2000)
    bathrooms     = models.IntegerField()
    capacity      = models.IntegerField()
    country       = models.CharField(max_length=50)
    province      = models.CharField(max_length=50)
    city          = models.CharField(max_length=50)
    address1      = models.CharField(max_length=500)
    address2      = models.CharField(max_length=500)
    full_address  = models.CharField(max_length=1000)
    zipcode       = models.IntegerField()
    created       = models.DateTimeField(auto_now_add=True)
    check_in      = models.DateTimeField(auto_now=False, auto_now_add=False)
    check_out     = models.DateTimeField(auto_now=False, auto_now_add=False)
    facilities    = models.ManyToManyField('Facility', through='StayFacility', related_name='stay_facility')
    amenities     = models.ManyToManyField('Amenity', through='StayAmenity', related_name='stay_amenity')
    house_rules   = models.ManyToManyField('HouseRule', through='StayHouseRule', related_name='stay_houserule')

    class Meta:
        db_table = 'stays'

class Image(models.Model) :
    stay      = models.ForeignKey(Stay, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'images'

class Facility(models.Model) :
    names    = models.CharField(max_length=50)
    icon_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'facilities'

class StayFacility(models.Model) :
    stay     = models.ForeignKey(Stay, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    class Meta:
        db_table = 'stay_facilities'

class Amenity(models.Model) :
    name     = models.CharField(max_length=50)
    icon_url = models.URLField(max_length=2000)

    class Meta:
        db_table= 'amenities'

class StayAmenity(models.Model) :
    stay    = models.ForeignKey(Stay, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        db_table = 'stay_amenities'

class Category(models.Model) :
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'

class Subcategory(models.Model) :
    name     = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcategories'

class RentalType(models.Model) :
    name     = models.CharField(max_length=50)
    icon_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'rental_types'

class HouseRule(models.Model) :
    name        = models.CharField(max_length=100)
    icon_url    = models.URLField(max_length=2000)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'house_rules'

class StayHouseRule(models.Model):
    stay        = models.ForeignKey(Stay, on_delete=models.CASCADE)
    house_rule  = models.ForeignKey(HouseRule, on_delete=models.CASCADE)

    class Meta:
       db_table = 'stay_houserules'

class Room(models.Model) :
    stay     = models.ForeignKey(Stay, on_delete=models.CASCADE)
    name     = models.CharField(max_length=50)
    beds     = models.IntegerField()
    icon_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'rooms'
