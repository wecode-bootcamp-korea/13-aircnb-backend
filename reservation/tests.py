import json

from unittest.mock      import patch, MagicMock
from django.test        import TestCase
from django.test        import TestCase, Client

from reservation.models import Booking, Cancellation
from user.models        import User, Host
from stay.models        import Stay, Facility, Amenity, Category, Subcategory, RentalType, HouseRule, Image, StayFacility, StayAmenity, Room 


class ReservationsTest(TestCase):
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
            password           = 'qwer1234'
            )
        Host.objects.create(
            user         = 3,
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
            name     = 'full home',
            icon_url = www.woah.com
            )
        HouseRule.objects.create(
            name        = 'wow',
            title       = 'wow',
            icon_url    = www.woah.com,
            description = 'wow'
            )
        Stay.objects.create(
            name           = 'woah',
            price          = 2314,
            monthly_price  = 6666,
            subcategory_id = 1,
            stay_type_id   = 1,
            host_id        = 1,
            latitude       = 1.11,
            longitude      = 1.11,
            description    = 'woah',
            bathrooms      = 4,
            capacity       = 5,
            country        = 'India',
            province       = 'woah',
            city           = 'woah',
            address        = 'woah',
            zipcode        = '122212',
            check_in       = '2020-11-11 15:00:00',
            check_out      = '2020-11-11 12:00:00',
            )
        Image.objects.create(
            stay_id   = 1,
            image_url = www.www.woah.com
            )
        StayFacility.objects.create(
            stay_id     = 1,
            facility_id = 1
            )
        StayAmenity.objects.create(
            stay_id    = 1,
            amenity_id = 1
            )
        Room.objects.create(
            stay_id = 1,
            name    = "woah",
            beds    = 5
            )
        Booking.objects.create(
            stay_id       = 1,
            guest_id      = 1,
            checkin_date  = "2020-12-10",
            checkout_date = "2020-12-15",
            guest_number  = 2,
            price         = 1000,
            creditcard    = "111111111111"
            )
        Cancellation.objects.create(
            booking_id = 1,
            user_id    = 1)

    def tearDown(self) :
        User.objects.all().delete()
        Host.objects.all().delete()
        Facility.objects.all().delete()
        Amenity.objects.all().delete()
        Category.objects.all().delete()
        Subcategory.objects.all().delete()
        RentalType.objects.all().delete()
        HouseRule.objects.all().delete()
        Stay.objects.all().delete()
        Image.objects.all().delete()
        StayFacility.objects.all().delete()
        StayAmenity.objects.all().delete()
        Room.objects.all().delete()
        Booking.objects.all().delete()
        Cancellation.objects.all().delete()

    def test_reservation_post_success(self, mocked_requests):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client           = Client()
        test             = {'email'    : 'schaubster@gmail.com' , 'password' : 'qwer1234' }
        response         = c.post('/user/signin', json.dumps(test), content_type='application/json')
        data             = {
                "stay"          : "1",
                "checkin_date"  : "2020-12-10",
                "checkout_date" : "2020-12-12",
                "guest_number"  : "2",
                "price"         : "100000",
                "creditcard"    : "1111111111111111"
                }
        access_token     = response.json()['AUTHORIZATION']
        response         = client.post('reservation/booking', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_reservation_post_no_login(self, mocked_requests):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client           = Client()
        test             = {'email'    : 'welford@wilshire.com' , 'password' : 'qwer1234' }
        response         = c.post('/user/signin', json.dumps(test), content_type='application/json')
        data             = {
                "stay"          : "1",
                "checkin_date"  : "2020-12-10",
                "checkout_date" : "2020-12-12",
                "guest_number"  : "2",
                "price"         : "100000",
                "creditcard"    : "1111111111111111"
                }
        access_token     = response.json()['AUTHORIZATION']
        response         = client.post('reservation/booking', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_reservation_post_wrong_key(self, mocked_requests):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client           = Client()
        test             = {'email'    : 'schaubster@gmail.com' , 'password' : 'qwer1234' }
        response         = c.post('/user/signin', json.dumps(test), content_type='application/json')
        data             = {
                "stayings"          : "1",
                "checkin_date"  : "2020-12-10",
                "checkout_date" : "2020-12-12",
                "guest_number"  : "2",
                "price"         : "100000",
                "creditcard"    : "1111111111111111"
                }
        access_token     = response.json()['AUTHORIZATION']
        response         = client.post('reservation/booking', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_reservation_no_stay(self, mocked_requests):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client           = Client()
        test             = {'email'    : 'schaubster@gmail.com' , 'password' : 'qwer1234' }
        response         = c.post('/user/signin', json.dumps(test), content_type='application/json')
        data             = {
                "stay"          : "100000000000000",
                "checkin_date"  : "2020-12-10",
                "checkout_date" : "2020-12-12",
                "guest_number"  : "2",
                "price"         : "100000",
                "creditcard"    : "1111111111111111"
                }
        access_token     = response.json()['AUTHORIZATION']
        response         = client.post('reservation/booking', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type' : 'application/json'})
        self.assertEqual(response.status_code, 400)