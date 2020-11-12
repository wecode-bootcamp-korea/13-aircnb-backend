from django.urls import path, include

urlpatterns = [
    path('review', include('review.urls')),
    path('user', include('user.urls')),
]
