from django.contrib import admin
from .models import Agency

# Register your models here.


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('ag_name', 'ag_tel', 'ag_brief')
    search_fields = ('ag_name',)
    list_filter = ('ag_name',)

    fieldsets = (
        (None, {
            'fields': ('ag_name', 'ag_tel', 'ag_brief')
        }),
    )
