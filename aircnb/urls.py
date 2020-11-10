from django.urls import path, include

urlpatterns = [
    path('review', include('review.urls')),
    path('user', include('user.urls')),
    path('stay', include('stay.urls')),
    path('reservation', include('reservation.urls')),
    path('homelist', include('stay.urls'))
]
