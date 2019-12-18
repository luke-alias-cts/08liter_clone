from django.urls import path
from .views      import SignupView, ShopInformationView, GoogleLogInView
urlpatterns = [
    path('/google', GoogleLogInView.as_view()),
    path('/signup', SignupView.as_view()),
    path('/shop', ShopInformationView.as_view()),
]
