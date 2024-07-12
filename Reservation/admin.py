from django.contrib import admin
from .models import Reservation

# Register your models here.


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('rv_date', 'tr_id', 'rt_rq_id', 'status')
    list_filter = ('rv_date', 'status')
    search_fields = ('tr_id__name', 'rt_rq_id__name')
