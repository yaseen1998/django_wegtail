from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import *

class FlexPageList(generics.ListCreateAPIView):
    queryset = FlexPage.objects.all()
    serializer_class = FlexPageSerializer