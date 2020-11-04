from django.db import models


class User(models.Model) :
	username          = models.CharField(max_length = 20)
	gender            = models.CharField(max_length = 10)
	email             = models.CharField(max_length = 50, unique=True)
	phone_number      = models.CharField(max_length = 14)
	emergency_contact = models.CharField(max_length = 14, null=True)
	introduction      = models.CharField(max_length = 300, null=True)
	image_url         = models.URLField(max_length = 2000, null=True)
	address           = models.CharField(max_length = 100)
	date_of_birth     = models.DateField(auto_now = False, auto_now_add = False)
	password          = models.CharField(max_length = 500)
	created_at        = models.DateTimeField(auto_now_add = True)
	update_at         = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'users'

class Host(models.Model) :
	user         = models.OneToOneField('User', on_delete = models.CASCADE)
	is_verified  = models.BooleanField()
	is_superhost = models.BooleanField()

	class Meta:
		db_table = 'hosts'