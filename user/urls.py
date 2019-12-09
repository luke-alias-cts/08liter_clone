from django.urls import path
from .views      import SignupView, ShopInformationView
urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/shopinformation', ShopInformationView.as_view())
]
