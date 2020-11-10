import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q, Avg, Sum, Max, Count

from stay.utils         import login_decorator
from user.models        import User, Host, Like
from review.models      import Review
from stay.models        import (
    Stay,
    RentalType,
    Amenity,
    StayAmenity,
    Category,
    Subcategory,
    HouseRule,
    StayHouseRule,
    Room
)

# 숙소 디테일 뷰
class StayDetailView(View):
    @login_decorator
    def get(self, request, stay_id):
        try:
            limit  = int(request.GET.get("limit", "6"))
            offset = int(request.GET.get("offset", "0"))
            stays  = Stay.objects.select_related(
                "subcategory",
                "host"
            ).prefetch_related(
                "review_set",
                "image_set",
                "room_set",
                "amenities",
                "house_rules"
            )
            stay      = stays.get(id = stay_id)
            detail = [
                {
                "id"            : stay.id,
                "name"          : stay.name,
                "province"      : stay.province,
                "city"          : stay.city,
                "address1"      : stay.address1,
                "address2"      : stay.address2,
                "latitude"      : float(stay.latitude),
                "longitude"     : float(stay.longitude),
                "price"         : int(stay.price),
                "discount_price": int(stay.discount_price),
                "capacity"      : stay.capacity,
                "subcategory"   : stay.subcategory.name,
                "beds"          : stay.room_set.aggregate(Sum("beds"))["beds__sum"],
                "rooms"         : stay.room_set.all().count(),
                "bathrooms"     : stay.bathrooms,
                "imgUrl"        : [ image.image_url for image in stay.image_set.all() ],
                "desc"          : stay.description,
                "houseRules"    : [
                    {
                        "icon"          : houserule.icon_url,
                        "title"         : houserule.name,
                        "desc"          : houserule.description
                    } for houserule in stay.house_rules.all()
                ],
                "facilities"    : [
                    {
                        "id"            : amenity.id,
                        "amenity"       : amenity.name,
                        "img"           : amenity.icon_url
                    } for amenity in stay.amenities.all()
                ],
                "bedType"       : [
                    {
                        "icon"          : room.icon_url,
                        "rooms"         : room.name,
                        "beds"          : room.beds
                    } for room in stay.room_set.all()
                ],
                "review"        : {
                    "avr_score"     : (
                        stay.review_set.aggregate(Avg("cleanliness_star"))["cleanliness_star__avg"]+
                        stay.review_set.aggregate(Avg("communication_star"))["communication_star__avg"]+
                        stay.review_set.aggregate(Avg("checkin_star"))["checkin_star__avg"]+
                        stay.review_set.aggregate(Avg("accuracy_star"))["accuracy_star__avg"]+
                        stay.review_set.aggregate(Avg("location_star"))["location_star__avg"]+
                        stay.review_set.aggregate(Avg("value_star"))["value_star__avg"]
                    ) / 6,
                    "reviews"       : stay.review_set.count(),
                    "userReviews"   : [
                        {
                            "userImg"   : User.objects.get(id=review.guest_id).image_url,
                            "userName"  : User.objects.get(id=review.guest_id).name,
                            "date"      : review.review_date,
                            "detail"    : review.body
                        } for review in stay.review_set.all()[offset:limit]
                    ]
                },
                "hostInfo"      : {
                    "img"           : User.objects.get(host__id = stay.host_id).image_url,
                    "name"          : User.objects.get(host__id = stay.host_id).name,
                    "hostId"        : stay.host_id,
                    "signUpDate"    : User.objects.get(host__id = stay.host_id).created_at,
                    "superHost"     : Host.objects.get(id = stay.host_id).is_superhost,
                    "verified"      : Host.objects.get(id = stay.host_id).is_verified,
                    "introduction"  : User.objects.get(host__id = stay.host_id).introduction
                }
            }
            ]
            return JsonResponse({"stay": detail},  status = 200)

        except Stay.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_PAGE"}, status = 400)

# 숙소 리스트 뷰
class StayListView(View):
    @login_decorator
    def get(self, request):
        try:
            place_id         = request.GET.get("place_id")
            checkin_date     = request.GET.get("checkin_date")
            checkout_date    = request.GET.get("checkout_date")
            adults           = request.GET.get("adults")
            children         = request.GET.get("children")
            infants          = request.GET.get("infants")
            bathrooms        = request.GET.get("bathrooms")
            beds             = request.GET.get("beds")
            rooms            = request.GET.get("rooms")
            offset           = int(request.GET.get("offset", 0))
            limit            = int(request.GET.get("limit", offset + 5))
            rental_type_id   = request.GET.getlist("rental_types")
            rental_type_dict = {"stay_type__in": rental_type_id}
            amenity_id       = request.GET.getlist("amenities")
            amenity_dict     = {"stayamenity__in": amenity_id}
            subcategory_id   = request.GET.getlist("subcategories")
            subcategory_dict = {"subcategory__in": subcategory_id}

            if children:
                adults = int(adults) + int(children)
            if infants:
                adults = int(adults) + int(infants)

            q = Q()
            if place_id:
                q.add(Q(full_address__icontains = place_id), q.AND)
            if adults:
                q.add(Q(capacity__gte = adults), q.AND)
            if bathrooms:
                q.add(Q(bathrooms__gte = bathrooms), q.AND)
            if beds:
                q.add(Q(sum_of_beds__gte = beds), q.AND)
            if rooms:
                q.add(Q(sum_of_rooms__gte = rooms), q.AND)

            # 렌탈타입, 편의시설, 집 종류를 필터링할 때
            if rental_type_id and amenity_id and subcategory_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **rental_type_dict
                ).filter(
                    **amenity_dict
                ).filter(
                    **subcategory_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 렌탈타입, 편의시설를 필터링할 때
            if rental_type_id and amenity_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **rental_type_dict
                ).filter(
                    **amenity_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 렌탈타입, 집 종류를 필터링할 때
            if rental_type_id and subcategory_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **rental_type_dict
                ).filter(
                    **subcategory_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 편의시설, 집 종류를 필터링할 때
            if amenity_id and subcategory_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **amenity_dict
                ).filter(
                    **subcategory_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 렌탈타입만 필터링할 때
            if rental_type_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **rental_type_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 편의시설만 필터링할 때
            if amenity_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **amenity_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            # 집 종류만 필터링할 때
            if subcategory_id:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q,
                    **subcategory_dict
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            else:
                stays = Stay.objects.annotate(
                    sum_of_beds  = Sum("room__beds"),
                    sum_of_rooms = Count("room__name")
                ).filter(
                    q
                ).select_related(
                    "host",
                    "subcategory"
                ).prefetch_related(
                    "room_set",
                    "review_set"
                )

            detail = [ {
                "id"            : stay.id,
                "name"          : stay.name,
                "province"      : stay.province,
                "city"          : stay.city,
                "address1"      : stay.address1,
                "address2"      : stay.address2,
                "full_address"  : stay.full_address,
                "latitude"      : int(stay.latitude),
                "longitude"     : int(stay.longitude),
                "price"         : int(stay.price),
                "discount_price": int(stay.discount_price),
                "subcategory"   : stay.subcategory.name,
                "capacity"      : stay.capacity,
                "beds"          : stay.room_set.aggregate(Sum("beds"))["beds__sum"],
                "rooms"         : stay.room_set.all().count(),
                "has_like"      : Like.objects.filter(
                    user_id = request.user.id,
                    stay_id = stay.id
                ).exists() if request.user else "GEUST",
                "review"        : {
                    "avr_score"     :(
                        stay.review_set.aggregate(Avg("cleanliness_star"))["cleanliness_star__avg"]+
                        stay.review_set.aggregate(Avg("communication_star"))["communication_star__avg"]+
                        stay.review_set.aggregate(Avg("checkin_star"))["checkin_star__avg"]+
                        stay.review_set.aggregate(Avg("accuracy_star"))["accuracy_star__avg"]+
                        stay.review_set.aggregate(Avg("location_star"))["location_star__avg"]+
                        stay.review_set.aggregate(Avg("value_star"))["value_star__avg"]
                    ) / 6,
                    "reviews"       : stay.review_set.count(),
                },
                "bathrooms"     : stay.bathrooms,
                "imgUrl"        : [ image.image_url for image in stay.image_set.all().select_related("stay") ],
            } for stay in stays[offset:limit] ]
            return JsonResponse({"stay": list(detail)}, status=200)

        except Stay.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_PAGE"}, status=400)
