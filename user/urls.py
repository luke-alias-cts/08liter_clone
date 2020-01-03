from django.urls import path
from .views      import SignupView, ShopInformationView, SignInView, KakaoSignInView, FacebookSignInView, GoogleLogInView
urlpatterns = [
    path('/google', GoogleLogInView.as_view()),
    path('/signup', SignupView.as_view()),
    path('/shop', ShopInformationView.as_view()),
    path('/shopinformation', ShopInformationView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/signin/kakao', KakaoSignInView.as_view()),
    path('/signin/facebook', FacebookSignInView.as_view()),
]
