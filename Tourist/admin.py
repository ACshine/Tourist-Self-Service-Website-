from django.contrib import admin
from .models import Tourist, FrequentTraveler

@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'user_type', 'is_sign_in']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['user_type', 'is_sign_in']
    ordering = ['user__username']
    fieldsets = (
        (None, {'fields': ('user', 'avatar', 'user_type', 'is_sign_in')}),
    )

@admin.register(FrequentTraveler)
class FrequentTravelerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone_number', 'id_type', 'id_number', 'nationality', 'gender']
    search_fields = ['name', 'user__user__username', 'phone_number', 'id_number']
    list_filter = ['id_type', 'gender']
    ordering = ['user__user__username']
    fieldsets = (
        (None, {'fields': ('user', 'name', 'phone_number', 'id_type', 'id_number', 'nationality', 'gender')}),
    )
