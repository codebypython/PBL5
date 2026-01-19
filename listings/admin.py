"""
Admin configuration for listings app.
"""
from django.contrib import admin
from .models import Category, Listing, ListingImage, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'status', 'created_at')
    list_filter = ('status', 'condition', 'category', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('seller',)
    inlines = [ListingImageInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'listing')
