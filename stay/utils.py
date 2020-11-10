import jwt
import json
import requests

from django.http                import JsonResponse
from django.core.exceptions     import ObjectDoesNotExist

from my_settings                import SECRET_KEY,ALGORITHM
from user.models                import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            encode_token = request.headers.get('Authorization')
            if encode_token:
                data = jwt.decode(
                    encode_token,
                    SECRET_KEY,
                    ALGORITHM
                )
                user = User.objects.get(id = data["user_id"])
                request.user = user
            else:
                request.user = False

        except jwt.exceptions.DecodeError :
            return JsonResponse({'ERROR_CODE' : 'INVALID_TOKEN'}, status = 401)
        except User.DoesNotExist :
            return JsonResponse({'ERROR_CODE' : 'UNKNOWN_USER'}, status = 401)

        return func(self, request, *args, **kwargs)
    return wrapper
