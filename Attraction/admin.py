from django.contrib import admin
from django.utils.html import format_html
from .models import Attraction, AttractionImage, Comment, CommentImage

class AttractionImageInline(admin.TabularInline):
    model = AttractionImage
    extra = 1

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" />'.format(obj.image.url))
        return ""
    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag']

    fields = ['image_tag', 'image']

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'star_level', 'rating', 'popularity', 'comment_count', 'address', 'official_phone']
    search_fields = ['name', 'address']
    list_filter = ['star_level', 'rating']
    ordering = ['name']
    fieldsets = (
        (None, {'fields': ('name', 'star_level', 'rating', 'description', 'opening_hours', 'popularity', 'comment_count', 'address', 'official_phone')}),
    )
    inlines = [AttractionImageInline]

class CommentImageInline(admin.TabularInline):
    model = CommentImage
    extra = 1

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" />'.format(obj.image.url))
        return ""
    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag']

    fields = ['image_tag', 'image']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'attraction', 'created_at', 'rating', 'likes', 'is_featured']
    search_fields = ['user__username', 'attraction__name', 'comment_text']
    list_filter = ['rating', 'is_featured']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('user', 'attraction', 'comment_text', 'rating', 'likes', 'is_featured')}),
    )
    inlines = [CommentImageInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at',)
        return self.readonly_fields
