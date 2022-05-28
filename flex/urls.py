
from django.urls import path,include
from .views import *
urlpatterns = [
    path('list/',FlexPageList.as_view(), name="herocover"),
]