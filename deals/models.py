"""
Models for deals app.
"""
import uuid
from django.db import models
from django.conf import settings


class Offer(models.Model):
    """Offer model."""
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'offers'
        indexes = [
            models.Index(fields=['listing', 'status']),
            models.Index(fields=['buyer']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Offer {self.price} for {self.listing.title}"


class Deal(models.Model):
    """Deal model."""
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='deal')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals_as_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals_as_seller')
    offer = models.OneToOneField(Offer, on_delete=models.RESTRICT, related_name='deal')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'deals'
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['buyer']),
            models.Index(fields=['seller']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Deal for {self.listing.title}"


class Meetup(models.Model):
    """Meetup model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='meetups')
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'meetups'
        indexes = [
            models.Index(fields=['deal']),
            models.Index(fields=['scheduled_at']),
        ]
    
    def __str__(self):
        return f"Meetup for {self.deal.listing.title}"
