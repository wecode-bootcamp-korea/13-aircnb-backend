#OS
import json
import re
import bcrypt
import jwt
import requests
#DJANGO
from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from django.core.mail import send_mail
#USER MADE
from user.models         import User, Host
from stay.models         import Stay
from reservation.models  import Booking
from reservation.utils   import login_decorator
from my_settings         import SECRET_KEY, ALGORITHM 
from reservation.utils   import login_decorator
from aircnb.settings     import EMAIL_HOST_USER

class Reservation(View) :

    @login_decorator 
    def post(self, request) :
        try :
            user_id = request.user.id
            data    = json.loads(request.body)
            print(data)
            Booking.objects.get_or_create(
                stay_id       = data['stay'],
                guest_id      = user_id,
                checkin_date  = data['checkin_date'],
                checkout_date = data['checkout_date'],
                guest_number  = data['guest_number'],
                price         = data['price'],
                creditcard    = data['creditcard']
            )
            book_user = User.objects.get(id = user_id)
            book_email = book_user.email
            book_username = book_user.name
            send_mail (
                'Your AirCnB is booked.',
                f'Dear {book_username}, \n\n\tThank you, {book_username}, for your money. We will spend it wisely on chicken and beer. \nIf you have any questions about checkin please feel free to crack a beer and hole up until 2020 keels over. \nYou can make any further unquiries by contacting the aircnb team by opening your windows explorer and releasing your mail pigeon. \n \
                \n \
                \nWith love,\nThe AirCnB team' ,
                EMAIL_HOST_USER,
                [f'{book_email}'],
                fail_silently = False
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEYERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "CHECK_USERNAME_PASSWORD"}, status=400)



class Cancellation(View) :

    @login_decorator
    def post(self, request, booking_id) :
        try:
            user_id = request.user.id
            data = json.loads(request.body)
            Cancellation.objects.create(
                                        booking     = data['booking_id'],
                                        user        = user_id,
                                        )
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER_NONEXISTANT'}, status = 400)    