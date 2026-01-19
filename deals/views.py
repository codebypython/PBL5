"""
Views for deals app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Offer, Deal, Meetup
from .serializers import OfferSerializer, DealSerializer, MeetupSerializer
from listings.models import Listing


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for Offer model."""
    queryset = Offer.objects.select_related('listing', 'buyer')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Filter offers."""
        queryset = Offer.objects.all()
        listing_id = self.request.query_params.get('listing_id')
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, id=None):
        """Accept an offer and create a deal."""
        offer = self.get_object()
        
        if offer.listing.seller != request.user:
            return Response(
                {'error': 'Only the seller can accept offers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if offer.status != Offer.Status.PENDING:
            return Response(
                {'error': 'Offer already processed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if offer.listing.status != Listing.Status.AVAILABLE:
            return Response(
                {'error': 'Listing is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Update offer status
            offer.status = Offer.Status.ACCEPTED
            offer.save()
            
            # Reject other offers
            Offer.objects.filter(
                listing=offer.listing,
                status=Offer.Status.PENDING
            ).exclude(id=offer.id).update(status=Offer.Status.REJECTED)
            
            # Create deal
            deal = Deal.objects.create(
                listing=offer.listing,
                buyer=offer.buyer,
                seller=offer.listing.seller,
                offer=offer
            )
            
            # Update listing status
            offer.listing.status = Listing.Status.RESERVED
            offer.listing.save()
        
        return Response({
            'message': 'Offer accepted, deal created',
            'offer': OfferSerializer(offer).data,
            'deal': DealSerializer(deal).data
        })


class DealViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Deal model."""
    queryset = Deal.objects.select_related('listing', 'buyer', 'seller', 'offer')
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Filter deals for current user."""
        return Deal.objects.filter(
            buyer=self.request.user
        ) | Deal.objects.filter(
            seller=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def meetups(self, request, id=None):
        """Create a meetup for a deal."""
        deal = self.get_object()
        serializer = MeetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(deal=deal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
