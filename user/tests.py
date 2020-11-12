from django.test import TestCase

import json

import bcrypt

from user.models   import User, Like, Host
from stay.models  import Stay
from django.test   import TestCase
from django.test   import Client
from unittest.mock import patch, MagicMock


class UserSignUp(TestCase):

    def setUp(self) :

        User.objects.create(
            name               = 'Brendan Schaub',
            gender             = 'Male',
            email              = 'schaubster@gmail.com',
            phone_number       = '01032321234',
            emergency_contact  = '01033993333',
            introduction       = 'Im just a small town girl, living in a lonely world',
            image_url          = 'https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python',
            address            = '경기도 황포시 강구대로 188-12',
            date_of_birth      = '1990-11-06',
            password           = '889dnv92!'
            )

        Host.objects.create(
            user_id = 1,
            is_verified = True,
            is_superhost = True
            )

        Facility.objects.create(
            names    = 'jacuzzi',
            icon_url = 'www.woah.com',
            )

        Amenity.objects.create(
            name     = 'hairdryer',
            icon_url = www.woah.com
            )

        Category.objects.create(
            name = 'yurt'
            )

        Subcategory.objects.create(
            name = 'subcategory'
            )

        RentalType.objects.create(
            name = 'full home',
            icon_url = www.woah.com
            )

        HouseRule.objects.create(
            name  = 'wow',
            title = 'wow',
            icon_url = www.woah.com,
            description = 'wow'
            )

        Stay.objects.create(
            name = 'woah',
            price = 2314,
            monthly_price = 6666,
            subcategory_id = 1,
            stay_type_id = 1,
            host_id = 1,
            latitude = 1.11,
            longitude = 1.11,
            description = 'woah',
            bathrooms = 4,
            capacity = 5,
            country = 'India',
            province = 'woah',
            city = 'woah',
            address = 'woah',
            zipcode = '122212',
            check_in = "2020-05-12",
            check_out = "2020-12-12",
            )

        Image.objects.create(
            stay_id = 1,
            image_url = www.www.woah.com
            )

        StayFacility.objects.create(
            stay_id = 1,
            facility_id = 1\
            )

        StayAmenity.objects.create(
            stay_id = 1,
            amenity_id = 1,
            )

        Room.objects.create(
            stay_id = 1,
            name = "woah",
            beds = 5
            )

    def tearDown(self) :
        User.objects.all().delete()
        Host.objects.all().delete()
        Facility.objects.all().delete()
        Amenity.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        RentalType.objects.all().delete()
        Stay.objects.all().delete()
        Image.objects.all().delete()
        StayFacility.objects.all().delete()
        StayAmenity.objects.all().delete()
        Room.objects.all().delete()


    def test_UserSignup_success(self):
        client = Client()
        user   = {
            name               : 'Brendan Schaub',
            gender             : 'Male',
            email              : 'schaubster1@gmail.com',
            phone_number       : '01032321234',
            emergency_contact  : '01033993333',
            introduction       : 'Im just a small town girl, living in a lonely world',
            image_url          : 'https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python',
            address            : '경기도 황포시 강구대로 188-12',
            date_of_birth      : '1990-11-06',
            password           : '889dnv92!'
        }
        response = client.post('/user/signup' , json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_UserSignUp_NoEmail(self):
        client = Client()
        user   = {
            name               : 'Brendan Schaub',
            gender             : 'Male',
            phone_number       : '01032321234',
            emergency_contact  : '01033993333',
            introduction       : 'Im just a small town girl, living in a lonely world',
            image_url          : 'https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python',
            address            : '경기도 황포시 강구대로 188-12',
            date_of_birth      : '1990-11-06',
            password           : '889dnv92!'
        }
        response = client.post('/user/signup' , json.dumps(user), content_type ='application/json')

        self.assertEqual(response.status_code, 400)

    def test_UserSignup_Email_Overlap(self):
        client = Cient()

        user2 = {
            name               : 'Brendan Schaub',
            gender             : 'Male',
            email              : 'schaubster@gmail.com',
            phone_number       : '01032321234',
            emergency_contact  : '01033993333',
            introduction       : 'Im just a small town girl, living in a lonely world',
            image_url          : 'https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python',
            address            : '경기도 황포시 강구대로 188-12',
            date_of_birth      : '1990-11-06',
            password           : '889dnv92!'
        }

        response2 = client.post('/user/signup' , json.dumps(user2), content_type ='application/json')
        self.assertEqual(response2.status_code, 400)

    def test_google_signup_success(self, mocked_requests) :
        client = Client()

        class MockedResponse :
            def json(self) :
                return {
                        'iss'            : 'accounts.google.com',
                        'azp'            : '1099506966197-9h0n051p5v9emnie5lhpaiua4p69dn40.apps.googleusercontent.com',
                        'aud'            : '1099506966197-9h0n051p5v9emnie5lhpaiua4p69dn40.apps.googleusercontent.com',
                        'sub'            : '102291767017405493680',
                        'email'          : 'vannskang@gmail.com',
                        'email_verified' : 'true',
                        'at_hash'        : 'QNyMOJVaH_IZwFZnBM7IKA',
                        'name'           : 'Vanns Kang',
                        'picture'        : 'https://lh3.googleusercontent.com/a-/AOh14Gg6piLV5bghlg2x6fjag_gr50CG9hYnQi4cgisPhA=s96-c',
                        'given_name'     : 'Vanns',
                        'family_name'    : 'Kang',
                        'locale'         : 'en',
                        'iat'            : '1605061977',
                        'exp'            : '1605065577',
                        'jti'            : 'c02e78bc4de74075dc8eafc630cd2be10a7e36a1',
                        'alg'            : 'RS256',
                        'kid'            : 'd946b137737b973738e5286c208b66e7a39ee7c1',
                        'typ'            : 'JWT'
                }
            mocked_requests.get = MagicMock(return_value = MockedResponse())
            response = client.post("/user/signin/google"**{'HTTP_AUTHORIZATION' : '12212' , 'content_type' : 'application/json' })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),{'AUTHORIZATION' : response.json()['AUTHORIZATION']})

    def test_google_signup_fail(self, mocked_requests) :
        client = Client()
        class MockedResponse :
            def json(self) :
                return {
                        'iss'            : 'accounts.google.com',
                        'azp'            : '1099506966197-9h0n051p5v9emnie5lhpaiua4p69dn40.apps.googleusercontent.com',
                        'aud'            : '1099506966197-9h0n051p5v9emnie5lhpaiua4p69dn40.apps.googleusercontent.com',
                        'sub'            : '102291767017405493680',
                        'email'          : 'vannskang@gmail.com',
                        'at_hash'        : 'QNyMOJVaH_IZwFZnBM7IKA',
                        'name'           : 'Vanns Kang',
                        'picture'        : 'https://lh3.googleusercontent.com/a-/AOh14Gg6piLV5bghlg2x6fjag_gr50CG9hYnQi4cgisPhA=s96-c',
                        'given_name'     : 'Vanns',
                        'family_name'    : 'Kang',
                        'locale'         : 'en',
                        'iat'            : '1605061977',
                        'exp'            : '1605065577',
                        'jti'            : 'c02e78bc4de74075dc8eafc630cd2be10a7e36a1',
                        'alg'            : 'RS256',
                        'kid'            : 'd946b137737b973738e5286c208b66e7a39ee7c1',
                        'typ'            : 'JWT'
                }
                mocked_requests.get = MagicMock(return_value = MockedResponse())
            response = client.post("/user/signin/google"**{'HTTP_AUTHORIZATION' : '12212' , 'content_type' : 'application/json' })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),{'MESSAGE' : response.json()['TOKEN_ERROR']})

    @patch('user.views.requests')
    def test_kakao_signup_success(self, mocked_requests) :
        client = Client()
        class MockedResponse :
            def json(self) :
                return {
                        'id'                        : 1525921852,
                        'connected_at'              : '2020-11-08T08:31:40Z',
                        'properties'                : {'nickname': 'soomyung'},
                        'kakao_account'             : {'profile_needs_agreement': False, 'profile': {'nickname': 'soomyung'},
                        'has_email'                 : True,
                        'email_needs_agreement'     : False,
                        'is_email_valid'            : True,
                        'is_email_verified'         : True,
                        'email'                     : 'michael.jordan@kakao.com',
                        'has_age_range'             : True,
                        'age_range_needs_agreement' : False,
                        'age_range'                 : '30~39'
                        }
                }
            mocked_requests.get = MagicMock(return_value = MockedResponse())
            header              = {"HTTP_Authorization" : token}
            response            = client.post('/account/phone-auth', json.dumps(user_info),  **header, content_type = 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),{'AUTHORIZATION' : response.json()['AUTHORIZATION']})

    @patch('user.views.requests')
    def test_kakao_signup_KeyError(self, mocked_requests) :
        client = Client()
        class MockedResponse :
            def json(self) :
                return {
                        'id'                        : 1525921852,
                        'connected_at'              : '2020-11-08T08:31:40Z',
                        'properties'                : {'nickname': 'soomyung'},
                        'kakao_account'             : {'profile_needs_agreement': False, 'profile': {'nickname': 'soomyung'},
                        'has_email'                 : True,
                        'email_needs_agreement'     : False,
                        'is_email_valid'            : True,
                        'is_email_verified'         : True,
                        'emai'                     : 'michael.jordan@kakao.com',
                        'has_age_range'             : True,
                        'age_range_needs_agreement' : False,
                        'age_range'                 : '30~39'
                        }
                }
            mocked_requests.get = MagicMock(return_value = MockedResponse())
            header              = {"HTTP_Authorization" : token}
            response            = client.post('/account/phone-auth', json.dumps(user_info),  **header, content_type = 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(),{'AUTHORIZATION' : response.json()['AUTHORIZATION']})

#{'id': 1525921852, 'connected_at': '2020-11-08T08:31:40Z', 
# 'properties': {'nickname': 'soomyung'}, 
# 'kakao_account': {'profile_needs_agreement': False, 'profile': {'nickname': 'soomyung'}, 
# 'has_email': True, 'email_needs_agreement': False, 'is_email_valid': True, 'is_email_verified': True, 
# 'email': 'michael.jordan@kakao.com', 'has_age_range': True, 'age_range_needs_agreement': False, 'age_range': '30~39'}}

class LikeFunction(TestCase) :

    def setUp(self) :

        User.objects.create(
            name               = 'Brendan Schaub',
            gender             = 'Male',
            email              = 'schaubster@gmail.com',
            phone_number       = '01032321234',
            emergency_contact  = '01033993333',
            introduction       = 'Im just a small town girl, living in a lonely world',
            image_url          = 'https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python',
            address            = '경기도 황포시 강구대로 188-12',
            date_of_birth      = '1990-11-06',
            password           = '889dnv92!'
            )

        Host.objects.create(
            user_id      = 1,
            is_verified  = True,
            is_superhost = True
            )

        Facility.objects.create(
            names    = 'jacuzzi',
            icon_url = 'www.woah.com',
            )

        Amenity.objects.create(
            name     = 'hairdryer',
            icon_url = www.woah.com
            )

        Category.objects.create(
            name = 'yurt'
            )

        Subcategory.objects.create(
            name = 'subcategory'
            )

        RentalType.objects.create(
            name = 'full home',
            icon_url = www.woah.com
            )

        HouseRule.objects.create(
            name  = 'wow',
            title = 'wow',
            icon_url = www.woah.com,
            description = 'wow'
            )

        Stay.objects.create(
            name = 'woah',
            price = 2314,
            monthly_price = 6666,
            subcategory_id = 1,
            stay_type_id = 1,
            host_id = 1,
            latitude = 1.11,
            longitude = 1.11,
            description = 'woah',
            bathrooms = 4,
            capacity = 5,
            country = 'India',
            province = 'woah',
            city = 'woah',
            address = 'woah',
            zipcode = '122212',
            check_in = "2020-05-12",
            check_out = "2020-12-12",
            )

        Image.objects.create(
            stay_id = 1,
            image_url = www.www.woah.com
            )

        StayFacility.objects.create(
            stay_id = 1,
            facility_id = 1\
            )

        StayAmenity.objects.create(
            stay_id = 1,
            amenity_id = 1,
            )

        Room.objects.create(
            stay_id = 1,
            name = "woah",
            beds = 5
            )

        Like.objects.create(
            stay_id = 1,
            user_id = 1
            )

    def tearDown(self) :
        User.objects.all().delete()
        Host.objects.all().delete()
        Facility.objects.all().delete()
        Amenity.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        RentalType.objects.all().delete()
        Stay.objects.all().delete()
        Image.objects.all().delete()
        StayFacility.objects.all().delete()
        StayAmenity.objects.all().delete()
        Room.objects.all().delete()
        Like.objects.all().delete()


