"""
Views for admin panel app.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from moderation.models import Report
from accounts.models import User
from listings.models import Listing
from core.permissions import IsAdmin
from .serializers import ReportListSerializer, ResolveReportSerializer


class ReportListView(generics.ListAPIView):
    """List all reports for admin."""
    queryset = Report.objects.filter(status=Report.Status.PENDING).order_by('-created_at')
    serializer_class = ReportListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ResolveReportView(generics.UpdateAPIView):
    """Resolve a report."""
    queryset = Report.objects.all()
    serializer_class = ResolveReportSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        report = self.get_object()
        action = request.data.get('action')
        
        if action == 'DISMISS':
            report.status = Report.Status.DISMISSED
        elif action == 'BAN_USER':
            if report.reported_user:
                report.reported_user.status = User.Status.BANNED
                report.reported_user.save()
                Listing.objects.filter(seller=report.reported_user).update(status=Listing.Status.EXPIRED)
            report.status = Report.Status.RESOLVED
        elif action == 'REMOVE_LISTING':
            if report.reported_listing:
                report.reported_listing.delete()
            report.status = Report.Status.RESOLVED
        
        report.resolved_by = request.user
        report.resolved_at = timezone.now()
        report.save()
        
        return Response({
            'message': 'Report resolved',
            'report': ReportListSerializer(report).data
        })


class BanUserView(generics.UpdateAPIView):
    """Ban a user."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.status = User.Status.BANNED
        user.save()
        Listing.objects.filter(seller=user).update(status=Listing.Status.EXPIRED)
        
        return Response({
            'message': 'User banned',
            'user': {
                'id': str(user.id),
                'email': user.email,
                'status': user.status
            }
        })
