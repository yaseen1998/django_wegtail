from rest_framework import serializers
from .models import *

class FlexPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexPage
        fields = "__all__"