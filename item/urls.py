from django.urls import path
from item.views  import ItemView

urlpatterns = [
    path('/detail', ItemView.as_view()),
]
