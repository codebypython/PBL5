"""
Views for listings app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Listing, ListingImage, Favorite
from .serializers import CategorySerializer, ListingSerializer, ListingCreateSerializer
from core.permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category model."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for Listing model."""
    queryset = Listing.objects.select_related('seller', 'category').prefetch_related('images')
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'condition']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ListingCreateSerializer
        return ListingSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, id=None):
        """Add or remove favorite."""
        listing = self.get_object()
        
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                listing=listing
            )
            if created:
                return Response({'message': 'Added to favorites'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            Favorite.objects.filter(user=request.user, listing=listing).delete()
            return Response({'message': 'Removed from favorites'}, status=status.HTTP_200_OK)
