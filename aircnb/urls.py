from django.urls import path, include

urlpatterns = [
    path('reservation', include('reservation.urls'))
]
