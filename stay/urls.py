from django.urls    import path
from stay.views     import StayDetailView, StayListView

urlpatterns = [
    path('/<int:stay_id>', StayDetailView.as_view()),
    path('', StayListView.as_view()),
]
