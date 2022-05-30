from django.contrib import admin

# Register your models here.
from .models import Subscribers

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
    

class SubscriberAdmin(ModelAdmin):
    model = Subscribers
    manu_label = "Sub_sucriber"
    menu_icon = "placeholder"
    meun_order = 290
    add_to_settings_menu = False
    exclude_from_explode_menu = True
    list_display = ('email','full_name','date')
    search_fields = ('email','full_name')


modeladmin_register(SubscriberAdmin)