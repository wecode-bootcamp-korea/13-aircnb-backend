#OS
import json
import re
import bcrypt
import jwt
import requests
#DJANGO
from django.shortcuts import render
from django.views     import View
from my_settings      import SECRET_KEY, ALGORITHM 
#from user.utils       import login_decorator
#USER MADE
from user.models      import User, Host
from stay.models      import Stay


class Reservation(View) :

    #@login_decorator 

    def post(self, request) :
        
        try :
            #user_id = request.user.id
            user_id = 5
            data    = json.loads(request.body)
            Booking.objects.create(
                                    stay          = data['stay'],
                                    guest         = user_id,
                                    checkin_date  = data['checkin_date'],
                                    checkout_date = data['checkout_date'],
                                    guest_number  = data['guest_number'],
                                    price         = data['price'],
                                    creditcard    = data['creditcard'],
                                    )

        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)



class Cancellation(View) :

    #@login_decorator

    def post(self, request, reservation_id) :

        try:
            #user_id = request.user.id
            user_id = 5
            data = json.loads(request.body)

            Cancellation.objects.create(
                                        booking     = data['booking_id'],
                                        user        = user_id,
                                        )
        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)    