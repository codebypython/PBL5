"""
Serializers for accounts app.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model."""
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'phone', 'location', 'avatar', 'avatar_url', 'bio', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_avatar_url(self, obj):
        """Get avatar URL."""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'status', 'profile', 'created_at', 'updated_at')
        read_only_fields = ('id', 'role', 'status', 'created_at', 'updated_at')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'full_name')
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """Create user and profile."""
        validated_data.pop('password_confirm')
        full_name = validated_data.pop('full_name')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(password=password, **validated_data)
        Profile.objects.create(user=user, full_name=full_name)
        
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating profile."""
    
    class Meta:
        model = Profile
        fields = ('full_name', 'phone', 'location', 'bio', 'avatar')
    
    def update(self, instance, validated_data):
        """Update profile."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
