"""
Serializers for listings app.
"""
from rest_framework import serializers
from .models import Category, Listing, ListingImage, Favorite
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'parent', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ListingImageSerializer(serializers.ModelSerializer):
    """Serializer for ListingImage model."""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ListingImage
        fields = ('id', 'image', 'image_url', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_image_url(self, obj):
        """Get image URL."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""
    seller = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = (
            'id', 'seller', 'category', 'title', 'description', 'price',
            'condition', 'location', 'status', 'images', 'is_favorited',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'seller', 'status', 'created_at', 'updated_at')
    
    def get_is_favorited(self, obj):
        """Check if current user favorited this listing."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, listing=obj).exists()
        return False


class ListingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Listing."""
    category_id = serializers.UUIDField(write_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Listing
        fields = (
            'category_id', 'title', 'description', 'price',
            'condition', 'location', 'images'
        )
    
    def validate_images(self, value):
        """Validate images."""
        if len(value) == 0:
            raise serializers.ValidationError("At least one image is required.")
        if len(value) > 5:
            raise serializers.ValidationError("Maximum 5 images allowed.")
        return value
    
    def create(self, validated_data):
        """Create listing with images."""
        images = validated_data.pop('images', [])
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        
        listing = Listing.objects.create(
            category=category,
            seller=self.context['request'].user,
            **validated_data
        )
        
        for index, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                order=index
            )
        
        return listing
