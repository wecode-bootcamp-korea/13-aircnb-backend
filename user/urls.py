from django.urls import path
from .views import SignUpView, SignInView, GoogleAuth, KakaoAuth, Liker, LikeList


urlpatterns = [
    path('/signup' , SignUpView.as_view()),
    path('/signin' , SignInView.as_view()),
    path('/signin/google' , GoogleAuth.as_view()),
    path('/signin/kakao', KakaoAuth.as_view()),
    path('/like' , Liker.as_view()),
    path('/likelist' , LikeList.as_view())
    ]