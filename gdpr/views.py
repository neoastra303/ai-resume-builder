from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import UserDataDeletionRequest, DataAccessRequest, DataRetentionSettings


@login_required
def gdpr_dashboard(request):
    """
    Dashboard for users to manage their GDPR rights
    """
    # Get user's data deletion requests
    deletion_requests = UserDataDeletionRequest.objects.filter(user=request.user).order_by('-requested_at')
    
    # Get user's data access requests
    access_requests = DataAccessRequest.objects.filter(user=request.user).order_by('-requested_at')
    
    # Get data retention settings
    retention_settings = DataRetentionSettings.objects.first()
    
    context = {
        'deletion_requests': deletion_requests,
        'access_requests': access_requests,
        'retention_settings': retention_settings,
    }
    
    return render(request, 'gdpr/dashboard.html', context)


@login_required
def request_data_deletion(request):
    """
    Allow users to request data deletion
    """
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        # Check if user already has an active deletion request
        existing_request = UserDataDeletionRequest.objects.filter(
            user=request.user,
            status__in=['requested', 'processing']
        ).first()
        
        if existing_request:
            messages.warning(request, 'You already have an active deletion request.')
        else:
            # Create deletion request
            deletion_request = UserDataDeletionRequest.objects.create(
                user=request.user,
                reason=reason
            )
            
            # Schedule deletion based on settings
            deletion_request.schedule_deletion()
            
            messages.success(request, 'Your data deletion request has been submitted. You will receive a confirmation email shortly.')
            
        return redirect('gdpr_dashboard')
    
    return render(request, 'gdpr/request_deletion.html')


@login_required
def cancel_data_deletion(request, request_id):
    """
    Allow users to cancel a data deletion request
    """
    try:
        deletion_request = UserDataDeletionRequest.objects.get(
            id=request_id,
            user=request.user,
            status='processing'
        )
        
        deletion_request.cancel_deletion()
        messages.success(request, 'Your data deletion request has been cancelled.')
    except UserDataDeletionRequest.DoesNotExist:
        messages.error(request, 'Invalid request or request not found.')
    
    return redirect('gdpr_dashboard')


@login_required
def request_data_access(request):
    """
    Allow users to request a copy of their data
    """
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        # Create data access request
        DataAccessRequest.objects.create(
            user=request.user,
            reason=reason
        )
        
        messages.success(request, 'Your data access request has been submitted. We will process your request and send you a download link shortly.')
        
        return redirect('gdpr_dashboard')
    
    return render(request, 'gdpr/request_access.html')