import os
import django
import csv
import sys
import bcrypt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aircnb.settings")
django.setup()

from user.models        import *
from stay.models        import *
from reservation.models import *
from review.models      import *

#CSV_PATH_USERS = "./01_users.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            User.objects.create(
#                name                = row[0],
#                gender              = row[1],
#                email               = row[2],
#                phone_number        = row[3],
#                emergency_contact   = row[4],
#                introduction        = row[5],
#                image_url           = row[6],
#                address             = row[7],
#                date_of_birth       = row[8],
#                password            = row[9]
#            )

#CSV_PATH_USERS = "./02_categories.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Category.objects.create(
#                name            = row[0],
#            )

#CSV_PATH_USERS = "./03_subcategories.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Subcategory.objects.create(
#                id              = row[0],
#                category_id     = row[1],
#                name            = row[2]
#            )

#CSV_PATH_USERS = "./04_stays.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Stay.objects.create(
#                name            = row[0],
#                price           = row[1],
#                discount_price  = row[2],
#                subcategory_id  = row[3],
#                stay_type_id    = row[4],
#                latitude        = row[5],
#                longitude       = row[6],
#                bathrooms       = row[7],
#                capacity        = row[8],
#                description     = row[9],
#                country         = row[10],
#                province        = row[11],
#                city            = row[12],
#                address1        = row[13],
#                address2        = row[14],
#                zipcode         = row[15],
#                check_in        = row[17],
#                check_out       = row[18],
#                host_id         = row[19]
#            )


#CSV_PATH_USERS = "./05_rental_types.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            RentalType.objects.create(
#                id              = row[0],
#                name            = row[1],
#                icon_url        = row[2],
#            )

#CSV_PATH_USERS = "./06_amenities.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Amenity.objects.create(
#                name            = row[0],
#                icon_url        = row[1],
#            )

#CSV_PATH_USERS = "./07_facilities.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Facility.objects.create(
#                names           = row[0],
#                icon_url        = row[1],
#            )


#CSV_PATH_USERS = "./08_house_rules.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            HouseRule.objects.create(
#                name            = row[0],
#                icon_url        = row[1],
#                description     = row[2]
#            )


#CSV_PATH_USERS = "./09_hosts.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Host.objects.create(
#                user_id         = row[0],
#                is_verified     = row[1],
#                is_superhost    = row[2],
#            )

#CSV_PATH_USERS = "./10_bookings.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Booking.objects.create(
#                stay_id         = row[0],
#                guest_id        = row[1],
#                checkin_date    = row[2],
#                checkout_date   = row[3],
#                guest_number    = row[4],
#                price           = row[5],
#                creditcard      = row[6],
#            )

#CSV_PATH_USERS = "./11_reviews.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Review.objects.create(
#                guest_id            = row[0],
#                host_id             = row[1],
#                stay_id             = row[2],
#                review_date         = row[3],
#                body                = row[4],
#                cleanliness_star    = row[5],
#                communication_star  = row[6],
#                checkin_star        = row[7],
#                accuracy_star       = row[8],
#                location_star       = row[9],
#                value_star          = row[10]
#            )

#CSV_PATH_USERS = "./12_stay_images.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Image.objects.create(
#                stay_id         = row[0],
#                image_url       = row[1]
#            )

#CSV_PATH_USERS = "./13_stays_amenities.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            StayAmenity.objects.create(
#                stay_id     = row[0],
#                amenity_id  = row[1]
#            )

#CSV_PATH_USERS = "./14_stays_facilities.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            StayFacility.objects.create(
#                stay_id     = row[0],
#                facility_id = row[1]
#            )

#CSV_PATH_USERS = "./15_stays_house_rules.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            StayHouseRule.objects.create(
#                stay_id       = row[0],
#                house_rule_id = row[1]
#            )
#
#CSV_PATH_USERS = "./16_rooms.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Room.objects.create(
#                stay_id = row[0],
#                name    = row[1],
#                beds    = row[2]
#            )
#
#CSV_PATH_USERS = "./17_likes.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Like.objects.create(
#                stay_id     = row[0],
#                wishlist_id = row[1]
#            )

#CSV_PATH_USERS = "./18_wishlist.csv"
#
#with open(CSV_PATH_USERS) as in_file:
#    data_reader = csv.reader(in_file)
#    next(data_reader, None)
#    for row in data_reader:
#        if row[0]:
#            Wishlist.objects.create(
#                name = row[0],
#                user_id = row[1]
#            )
