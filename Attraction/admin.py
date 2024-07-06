from django.contrib import admin
from .models import Attraction, Comment

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'star_level', 'rating', 'popularity', 'comment_count', 'address', 'official_phone']
    search_fields = ['name', 'address']
    list_filter = ['star_level', 'rating']
    ordering = ['name']
    fieldsets = (
        (None, {'fields': ('name', 'star_level', 'rating', 'description', 'opening_hours', 'popularity', 'comment_count', 'address', 'official_phone')}),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'attraction', 'created_at', 'rating', 'likes', 'is_featured']
    search_fields = ['user__username', 'attraction__name', 'comment_text']
    list_filter = ['rating', 'is_featured']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('user', 'attraction', 'created_at', 'comment_text', 'rating', 'likes', 'optional_image', 'is_featured')}),
    )
