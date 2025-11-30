from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # GDPR compliance fields
    consent_to_data_processing = models.BooleanField(
        default=False,
        help_text="Consent to data processing for resume building purposes"
    )
    consent_to_marketing_emails = models.BooleanField(
        default=False,
        help_text="Consent to receive marketing emails"
    )
    data_retention_end_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date when user data will be automatically deleted"
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        app_label = 'resume_builder'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name

    @property
    def is_gdpr_consent_given(self):
        """
        Check if user has given consent for data processing
        """
        return self.consent_to_data_processing