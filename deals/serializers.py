"""
Serializers for deals app.
"""
from rest_framework import serializers
from .models import Offer, Deal, Meetup
from accounts.serializers import UserSerializer
from listings.serializers import ListingSerializer


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for Offer model."""
    buyer = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    
    class Meta:
        model = Offer
        fields = ('id', 'listing', 'buyer', 'price', 'message', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'buyer', 'status', 'created_at', 'updated_at')


class MeetupSerializer(serializers.ModelSerializer):
    """Serializer for Meetup model."""
    
    class Meta:
        model = Meetup
        fields = ('id', 'deal', 'scheduled_at', 'location', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')


class DealSerializer(serializers.ModelSerializer):
    """Serializer for Deal model."""
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)
    meetups = MeetupSerializer(many=True, read_only=True)
    
    class Meta:
        model = Deal
        fields = (
            'id', 'listing', 'buyer', 'seller', 'offer', 'status',
            'meetups', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
