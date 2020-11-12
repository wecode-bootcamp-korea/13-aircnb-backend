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
from django.db.models import Sum, Avg

from user.models      import User, Host, Like
from stay.models      import Stay
from review.models    import Review
from my_settings      import SECRET_KEY, ALGORITHM 
from user.utils       import login_decorator


class SignUpView(View) :
    def post(self, request):
        data = json.loads(request.body)
        email_form    = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        password_form = '^[A-Za-z0-9]{6,}$'
        try:
            if not re.match(email_form, data['email']) :
                return JsonResponse({'MESSAGE' : 'EMAIL_FORM'}, status = 401)
            elif not re.match(password_form, data['password']) :
                return JsonResponse({'MESSAGE' : 'PASSWORD_FORM'}, status = 401)
            elif User.objects.filter(email = data['email']).exists() :
                return JsonResponse({'MESSAGE' : 'EMAIL_IN_USE'}, status = 401)
            else :
                User.objects.create(
                    email         = data['email'],
                    name          = data['name'],
                    phone_number  = data['phone_number'],
                    password      = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode(),
                    date_of_birth = data['date_of_birth']
                )
                return JsonResponse({'MESSAGE' : 'ACCOUNT_CREATED'}, status = 401)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 401)

class SignInView(View) :
    def post(self, request) :
        data = json.loads(request.body)
        try :
            if User.objects.filter(email = data['email']).exists() :
                account = User.objects.get(email = data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')) == True :
                    return JsonResponse({'MESSAGE' : 'SUCCESS' , 'AUTHORIZATION' : jwt.encode({'id' : account.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
        except account.DoesNotExist:
            return JsonResponse({'NO_USER'}, status = 400)
        except KeyError :
            return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)
        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)

class GoogleAuth(View) :
    def post(self, request) :
        try :
            data  = json.loads(request.body)
            token           = data['AUTHORIZATION']
            google_response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
            google_identity = google_response.json()
            if google_identity['email_verified'] :
                name                   = google_identity['name']
                email                  = google_identity['email']
                image_url              = google_identity['picture']
                google_login, created  = User.objects.get_or_create(email = google_identity['email'])
                google_login.name      = google_identity['name']
                google_login.image_url = google_identity['picture']
                google_login.save()
            return JsonResponse ({'MESSAGE' : 'GOOGLE_AUTH_SUCCESSFUL' , 'AUTHORIZATION' : jwt.encode({'id' : google_login.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
            if google_identity['email_verified'] == 'false' :
                return JsonResponse({'MESSAGE' : 'UNVERIFIED_GOODLE_TOKEN'})
        except KeyError:
            return JsonResponse({'MESSAGE':'TOKEN_ERROR'}, status = 400)
        except IndexError as e:
            return JsonResponse({"MESSAGE": f"ERROR{e}"}, status=400)

class KakaoAuth(View) :
    def get(self, request) :
        try :
            authorization        = request.headers.get('AUTHORIZATION')
            authorization_header = ({'AUTHORIZATION' : f'Bearer {authorization}'})
            kakao_response       = requests.get('https://kapi.kakao.com/v2/user/me', headers=authorization_header)
            kakao_identity       = kakao_response.json()
            nickname             = kakao_identity['kakao_account']['profile']['nickname']
            email                = kakao_identity['kakao_account']['email']
            kakao_login, created = User.objects.get_or_create(email = email)
            kakao_login.name     = nickname
            kakao_login.save()
            return JsonResponse({'MESSAGE' : 'KAKAO_AUTH_SUCCESSFUL' , 'AUTHORIZATION' : jwt.encode({'id' : kakao_login.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
        except authorization.DoesNotExist :
                return  JsonResponse({'MESSAGE' : 'NO_TOKEN'}, status = 400)
        except kakao_response.DoesNotExist :
                return JsonResponse({'MESSAGE' : 'NO_KAKAO_RESPONSE'}, status = 400)

class Liker(View) :
    @login_decorator
    def post(self, request) :
        try:
            user_id       = request.user.id
            data          = json.loads(request.body)
            stay          = data['stay_id']
            like, created = Like.objects.get_or_create(stay_id = stay, user_id = user_id)
            if created == False :
                like.delete()
                return JsonResponse({'SUCCESS' : 'UNLIKED'}, status = 202)
            if created == True :
                return  JsonResponse({'SUCCESS' : 'LIKED'}, status = 200)
        except stay.DoesNotExist:
                return JsonResponse({'MESSAGE' : 'STAY_DOESNT_EXIST'}, status = 400)
        except user_id.DoesNotExist :
                return JsonResponse({'MESSAGE' : 'USER_NOT_SIGNED_IN'}, status = 400)
        except KeyError :
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class LikeList(View) :
    @login_decorator
    def get(self, request) :
        try:
            user_id = request.user.id
            offset  = int(request.GET.get('offset', 0))
            limit   = int(request.GET.get('limit', offset + 5))
            stays   = Stay.objects.filter(like__user_id = user_id).select_related(
                'host',
                'subcategory').prefetch_related(
                                                'room_set',
                                                'image_set',
                                                'review_set',
                                                'like_set'
                                                )
            rating_stars = [
                'cleanliness_star',
                'communication_star',
                'checkin_star',
                'accuracy_star',
                'location_star',
                'value_star'
            ]

            liked_stays    = [{
                "id"             : stay.id,
                "name"           : stay.name,
                "province"       : stay.province,
                "city"           : stay.city,
                "address1"       : stay.address1,
                "address2"       : stay.address2,
                "latitude"       : stay.latitude,
                "longitude"      : stay.longitude,
                "price"          : stay.price,
                "discount_price" : stay.discount_price,
                "subcategory"    : stay.subcategory.name,
                "capacity"       : stay.capacity,
                "beds"           : stay.room_set.aggregate(Sum("beds"))['beds__sum'],
                "rooms"          : stay.room_set.all().count(),
                "bathrooms"      : stay.bathrooms,
                "has_like"       : Like.objects.filter(user_id = user_id, stay_id = stay.id).exists(),
                "imgUrl"         : [image.image_url for image in stay.image_set.all()],
                "review_count"   : stay.review_set.count(),
                "overall_star"   : sum([stay.review_set.aggregate(Avg(rating_star))[rating_star+'__avg'] for rating_star in rating_stars])/len(rating_stars)
            } for stay in stays[offset:limit] ]
            return JsonResponse({"stay": list(liked_stays)}, status=200)
            if not user_id :
                return JsonResponse({'MESSAGE' : 'USER_NOT_SIGNED_IN'}, status = 400)
        except Stay.DoesNotExist:
            return JsonResponse({"MESSAGE": "NOTFOUND"}, status=400)