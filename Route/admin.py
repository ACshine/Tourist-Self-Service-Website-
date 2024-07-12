from django.contrib import admin
from .models import Agency, Route

# Register your models here.


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('rt_name', 'ag_id', 'price', 'rt_brief')
    list_filter = ('ag_id',)
    search_fields = ('rt_name', 'rt_brief')
    ordering = ('rt_name',)
