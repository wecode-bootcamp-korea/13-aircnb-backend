from django.shortcuts import render

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
from django.db.models import F, Sum, FloatField, Avg

from user.models      import User, Host, Like
from stay.models      import Stay
from review.models    import Review
from my_settings      import SECRET_KEY, ALGORITHM 
from review.utils     import login_decorator


class ReviewView(View) :
    @login_decorator
    def get(self, request) :
        try:
            user_id           = request.user.id
            offset            = int(request.GET.get('offset', 0))
            limit             = int(request.GET.get('limit', offset + 5))
            stay_id           = int(request.GET['stay_id'])
            reviews           = Review.objects.filter(stay_id = stay_id).select_related('stay','guest')
            cleanliness_avg   = reviews.aggregate(Avg("cleanliness_star"))['cleanliness_star__avg']
            communication_avg = reviews.aggregate(Avg("communication_star"))['communication_star__avg']
            checkin_avg       = reviews.aggregate(Avg("checkin_star"))['checkin_star__avg']
            accuracy_avg      = reviews.aggregate(Avg("accuracy_star"))['accuracy_star__avg']
            location_avg      = reviews.aggregate(Avg("location_star"))['location_star__avg']
            value_avg         = reviews.aggregate(Avg("value_star"))['value_star__avg']

            review_overview   = {
                "review_count"    : reviews.count(),
                "overall_star"    : (cleanliness_avg+communication_avg+checkin_avg+accuracy_avg+location_avg+value_avg)/6,
                "avg_star_detail" : {
                    "cleanliness_star"   : cleanliness_avg,
                    "communication_star" : communication_avg,
                    "checkin_star"       : checkin_avg,
                    "accuracy_star"      : accuracy_avg,
                    "location_star"      : location_avg,
                    "value_star"         : value_avg
                                }

            }

            review_list    = [{
                "id"                 : review.id,
                "user_id"            : review.guest.id,
                "user_name"          : review.guest.name,
                "user_img"           : review.guest.image_url,
                "review_date"        : review.review_date,
                "review_body"        : review.body,
                "cleanliness_star"   : review.cleanliness_star,
                "communication_star" : review.communication_star,
                "checkin_star"       : review.checkin_star,
                "accuracy_star"      : review.accuracy_star,
                "location_star"      : review.location_star,
                "value_star"         : review.value_star
                } for review in reviews[offset:limit] ]

            return JsonResponse({"overall": review_overview, "review_list" : review_list}, status=200)
        except user_id.DoesNotExist:
            return JsonResponse({"MESSAGE": "LOGIN_PLEASE"}, status=400)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEYERROR"}, status=400)