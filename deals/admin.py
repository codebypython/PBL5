"""
Admin configuration for deals app.
"""
from django.contrib import admin
from .models import Offer, Deal, Meetup


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'buyer', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('listing__title',)
    raw_id_fields = ('listing', 'buyer')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'buyer', 'seller', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('listing__title',)
    raw_id_fields = ('listing', 'buyer', 'seller', 'offer')


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ('id', 'deal', 'scheduled_at', 'location', 'created_at')
    list_filter = ('scheduled_at', 'created_at')
    raw_id_fields = ('deal',)
