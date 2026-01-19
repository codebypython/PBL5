"""
Models for listings app.
"""
import uuid
from django.db import models
from django.conf import settings


class Category(models.Model):
    """Category model for listings."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    """Listing model for products."""
    
    class Condition(models.TextChoices):
        NEW = 'NEW', 'New'
        LIKE_NEW = 'LIKE_NEW', 'Like New'
        USED = 'USED', 'Used'
        POOR = 'POOR', 'Poor'
    
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        RESERVED = 'RESERVED', 'Reserved'
        SOLD = 'SOLD', 'Sold'
        EXPIRED = 'EXPIRED', 'Expired'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=Condition.choices)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'listings'
        indexes = [
            models.Index(fields=['seller']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'category']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return self.title


class ListingImage(models.Model):
    """Listing image model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'listing_images'
        ordering = ['order']
        indexes = [
            models.Index(fields=['listing', 'order']),
        ]
    
    def __str__(self):
        return f"{self.listing.title} - Image {self.order}"


class Favorite(models.Model):
    """Favorite model for user favorites."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favorites'
        unique_together = ['user', 'listing']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['listing']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.listing.title}"
