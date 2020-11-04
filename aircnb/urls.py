from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('stays', include('stays.urls')),
    path('reservations', include('reservations.urls')),
    path('wishlists', include('witshlists.urls')),
    path('reviews', include('reviews.urls')),
]
