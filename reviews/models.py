from django.db 	  import models

from users.models import User, Host
from stays.models import Stay


class Review(models.Model) :
	guest 				= models.ForeignKey('User', on_delete = models.CASCADE)
	host 				= models.ForeignKey('Host', on_delete = models.CASCADE)
	stay 				= models.ForeignKey('Stay', on_delete = models.CASCADE)
	review_date 		= models.DateField(auto_now = True, auto_now_add = False)
	body 				= models.CharField(max_length = 2000)
	cleanliness_star	= models.IntegerField()
	communication_star  = models.IntegerField()
	checkin_star 		= models.IntegerField()
	accuracy_star 		= models.IntegerField()
	location_star 		= models.IntegerField()
	value_star 			= models.IntegerField()

	class Meta:
		db_table= 'reviews'