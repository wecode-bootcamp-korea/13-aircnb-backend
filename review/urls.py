from django.urls import path
from .views      import ReviewView


urlpatterns = [
    path('/list',ReviewView.as_view()),
    ]
