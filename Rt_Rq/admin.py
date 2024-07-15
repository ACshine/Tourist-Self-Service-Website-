from django.contrib import admin
from .models import Rt_Rq

# Register your models here.


@admin.register(Rt_Rq)
class Rt_RqAdmin(admin.ModelAdmin):
    list_display = ('id', 'rt_id', 'rq', 'days', 'limit')
    list_filter = ('rt_id', 'rq')
    search_fields = ('rt_id__rt_name', 'rq')
    ordering = ('id', 'rq')  # 排序选项
