from django.db import models

from stay.models import Stay
from user.models import User, Host

class Booking(models.Model) :
    stay          = models.ForeignKey(Stay, on_delete = models.CASCADE)
    guest         = models.ForeignKey(User, on_delete = models.CASCADE)
    checkin_date  = models.DateField(auto_now = False, auto_now_add=False)
    checkout_date = models.DateField(auto_now = False, auto_now_add=False)
    guest_number  = models.IntegerField()
    price         = models.DecimalField(max_digits = 60, decimal_places = 2)
    creditcard    = models.CharField(max_length = 200)
    request_date  = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'bookings'

class Cancellation(models.Model) :
    booking     = models.ForeignKey('Booking', on_delete = models.CASCADE)
    user        = models.ForeignKey(User, on_delete = models.CASCADE)
    cancel_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'cancellations'
