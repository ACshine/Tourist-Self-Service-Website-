from django.contrib import admin
from .models import Rt_At

# Register your models here.


@admin.register(Rt_At)
class Rt_AtAdmin(admin.ModelAdmin):
    list_display = ['id', 'rt_id', 'at_id']
    list_filter = ['rt_id', 'at_id']
    search_fields = ['rt_id__rt_name', 'at_id__name']
