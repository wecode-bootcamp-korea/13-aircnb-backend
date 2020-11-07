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
from user.models      import User, Host
from my_settings      import SECRET_KEY, ALGORITHM 
from user.utils       import login_decorator
#USER MADE
from user.models      import User


class SignUpView(View) :

    def post(self, request):
        data = json.loads(request.body)
        email_form    = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        password_form = '^[A-Za-z0-9]{6,}$'

        try:
            if not re.match(email_form, data['email']) :
                return JsonResponse({'MESSAGE' : 'EMAIL_FORM'}, status = 401)
                print('1')

            elif not re.match(password_form, data['password']) :
                return JsonResponse({'MESSAGE' : 'PASSWORD_FORM'}, status = 401)
                print('2')
            
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
            print('5')

class SignInView(View) :

    def post(self, request) :
        data = json.loads(request.body)
        print(data)

        try :
            if User.objects.filter(email = data['email']).exists() :
                account = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')) == True :
                    return JsonResponse({'MESSAGE' : 'SUCCESS' , 'AUTHORIZATION' : jwt.encode({'id' : account.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
                
                else:
                    return JsonResponse({'MESSAGE' : 'EMAIL_PASSWORD_INVALID'}, status = 400)
            else:
                return JsonResponse({'MESSAGE' : 'EMAIL_DOES_NOT_EXIST'}, status = 400)

        except KeyError :
            return JsonResponse({'MESSAGE' : 'KEYERROR'}, status = 400)
        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)


class GoogleAuth(View) :

    def post(self, request) :
        
        try :
            data  = json.loads(request.body)
            token           = data['AUTHORIZATION']
            google_response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
            google_identity = google_response.json()
            print(google_identity)

            if google_identity['email_verified'] == 'true' :

                name            = google_identity['name']
                email           = google_identity['email']
                image_url       = google_identity['picture']

                google_login, created  = User.objects.get_or_create(email = google_identity['email'])

                google_login.name      = google_identity['name']
                google_login.image_url = google_identity['picture']
                google_login.save()

                return JsonResponse ({'MESSAGE' : 'GOOGLE_AUTH_SUCCESSFUL' , 'AUTHORIZATION' : jwt.encode({'id' : google_login.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
                
            else:
                return JsonResponse({'MESSAGE': 'UNVERIFIED_GOOGLE_PROFILE'})

        except KeyError:
            return JsonResponse({'MESSAGE':'TOKEN_ERROR'}, status = 400)


class KakaoAuth(View) :

    def get(self, request) :
        try :
            authorization        = request.headers.get('AUTHORIZATION')
            authorization_header = ({'AUTHORIZATION' : f'Bearer {authorization}'})
            kakao_response       = requests.get('https://kapi.kakao.com/v2/user/me', headers=authorization_header)
            kakao_identity       = kakao_response.json()

            try:
                nickname = kakao_identity['kakao_account']['profile']['nickname']
                email    = kakao_identity['kakao_account']['email']

                kakao_login, created = User.objects.get_or_create(email = email)
                kakao_login.name     = nickname
                kakao_login.save()

                return JsonResponse({'MESSAGE' : 'KAKAO_AUTH_SUCCESSFUL' , 'AUTHORIZATION' : jwt.encode({'id' : kakao_login.id}, SECRET_KEY, ALGORITHM).decode()}, status = 200)
            
            except KeyError:
                return JsonResponse({'MESSAGE' : 'TOKEN_ERROR'}, status = 400)
        except KeyError:
            return JsonResponse({'MESSAGE':'TOKEN_NOT_SENT'}, status = 400)
        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)


class WishList(View) :

    @login_decorator

    def post(self, request) :

        user_id = request.user.id
        data    = json.loads(request.body)
        name    = data['name']

        Wishlist.objects.create(user = user_id, name = name)

    def get(self, request) : 

        queryset_wishlist = Wishlist.objects.filter(user = user_id).select_related('user').prefetch_related('like_set__stay__image_set')

        rooms_in_wishlist = [{
                            'wishlist_id'    : wishlist.id,
                            'wishlist_name'  : wishlist.name,
                            'wishlist_stays' : [{
                                                'id'     : like.stay.id,
                                                'photos' : [photo.image_url for photo in like.stay.photo]
                                                } 
                                                for like in wishlist.like_set]
                            }
                            for wishlist in queryset_wishlist]


class Like(View) :

    @login_decorator

    def post(self, request) :
        
        try:
            user_id      = request.user.id
            data         = json.loads(request.body)
            stay         = data['stay_id']

            Like.objects.create(stay_id = stay, user_id = user_id)

        except KeyError:
            return JsonResponse ({'MESSAGE' : 'KEYERROR'})
        except Exception as e:
            return JsonResponse({'MESSAGE':f'ERROR {e}'}, status = 400)


class LikeList(View) :

    @login_decorator

    def get(self, request, wishlist_name) :

        try:
            user_id  = request.user.id
            queryset = Like.objects.filter(wishlist = wishlist_id).select_related('Wishlist','stay')
            [{ wishlist_id : {
                            'stay_id' : queryset.stay.id
                            }
            } for stays in queryset]
        except :
            print('1')