from django.db import models
from resume_builder.models import User
from django.utils import timezone
from datetime import timedelta


class DataRetentionSettings(models.Model):
    """
    Model to store data retention settings
    """
    id = models.AutoField(primary_key=True)
    retention_period_days = models.IntegerField(
        default=365,
        help_text="Number of days to retain user data after account deletion request or inactivity"
    )
    auto_delete_inactive_users = models.BooleanField(
        default=True,
        help_text="Automatically delete users who have been inactive for the retention period"
    )
    notify_before_deletion_days = models.IntegerField(
        default=30,
        help_text="Number of days before deletion to notify the user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Data Retention Setting"
        verbose_name_plural = "Data Retention Settings"

    def __str__(self):
        return f"Data Retention: {self.retention_period_days} days"


class UserDataDeletionRequest(models.Model):
    """
    Model to track user data deletion requests
    """
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(
        blank=True,
        help_text="Reason for requesting data deletion"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    deletion_scheduled_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Scheduled date for data deletion"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User Data Deletion Request"
        verbose_name_plural = "User Data Deletion Requests"

    def __str__(self):
        return f"Deletion Request for {self.user.email} - {self.status}"

    def schedule_deletion(self):
        """
        Schedule the user's data for deletion based on retention settings
        """
        settings = DataRetentionSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = DataRetentionSettings.objects.create()
            
        self.deletion_scheduled_at = timezone.now() + timedelta(days=settings.notify_before_deletion_days)
        self.status = 'processing'
        self.save()

    def cancel_deletion(self):
        """
        Cancel a scheduled deletion
        """
        self.status = 'cancelled'
        self.deletion_scheduled_at = None
        self.processed_at = timezone.now()
        self.save()

    def execute_deletion(self):
        """
        Execute the actual data deletion
        """
        # Mark the request as completed
        self.status = 'completed'
        self.deleted_at = timezone.now()
        self.processed_at = timezone.now()
        self.save()
        
        # Delete the user's resumes and related data
        # Note: We don't delete the user account itself to maintain referential integrity
        # but we anonymize the data
        from resumes.models import Resume
        
        # Anonymize user data
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.email = f"deleted_{self.user.id}@deleted.local"
        self.user.is_active = False
        self.user.consent_to_data_processing = False
        self.user.consent_to_marketing_emails = False
        self.user.data_retention_end_date = None
        self.user.save()
        
        # Delete user's resumes
        Resume.objects.filter(user=self.user).delete()


class DataAccessRequest(models.Model):
    """
    Model to track user data access requests (Right to Access)
    """
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(
        blank=True,
        help_text="Reason for requesting data access"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    data_file = models.FileField(
        upload_to='data_access_requests/',
        null=True, 
        blank=True,
        help_text="Exported user data file"
    )

    class Meta:
        verbose_name = "User Data Access Request"
        verbose_name_plural = "User Data Access Requests"

    def __str__(self):
        return f"Data Access Request for {self.user.email} - {self.status}"