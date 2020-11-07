from django.urls import path
from .views import SignUpView, SignInView, GoogleAuth, KakaoAuth, WishList, Like, LikeList


urlpatterns = [
    path('/signup' , SignUpView.as_view()),
    path('/signin' , SignInView.as_view()),
    path('/signin/google' , GoogleAuth.as_view()),
    path('/signin/kakao', KakaoAuth.as_view()),
    path('/wishlist/' , WishList.as_view()),
    path('/wishlist/like/<int:stay_id>' , Like.as_view()),
    path('/wishlist/list/<str:wishlist_name>' , LikeList.as_view())
    ]