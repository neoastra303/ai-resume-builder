from django.core.management.base import BaseCommand
from django.utils import timezone
from gdpr.models import UserDataDeletionRequest, DataRetentionSettings
from resume_builder.models import User


class Command(BaseCommand):
    help = 'Process scheduled data deletion requests'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get data retention settings
        settings = DataRetentionSettings.objects.first()
        if not settings:
            self.stdout.write(
                self.style.WARNING('No data retention settings found. Creating default settings.')
            )
            settings = DataRetentionSettings.objects.create()
        
        # Find deletion requests that are ready to be processed
        now = timezone.now()
        deletion_requests = UserDataDeletionRequest.objects.filter(
            status='processing',
            deletion_scheduled_at__lte=now
        )
        
        if not deletion_requests.exists():
            self.stdout.write(
                self.style.SUCCESS('No deletion requests ready for processing.')
            )
            return
        
        self.stdout.write(
            self.style.NOTICE(f'Found {deletion_requests.count()} deletion requests ready for processing.')
        )
        
        for request in deletion_requests:
            if dry_run:
                self.stdout.write(
                    f'DRY RUN: Would delete data for user {request.user.email}'
                )
            else:
                self.stdout.write(
                    f'Processing deletion request #{request.id} for user {request.user.email}'
                )
                try:
                    request.execute_deletion()
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully deleted data for user {request.user.email}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to delete data for user {request.user.email}: {str(e)}')
                    )
        
        # Handle inactive users if auto-delete is enabled
        if settings.auto_delete_inactive_users:
            retention_cutoff = now - timezone.timedelta(days=settings.retention_period_days)
            inactive_users = User.objects.filter(
                last_login__lte=retention_cutoff,
                is_active=True
            )
            
            if inactive_users.exists():
                self.stdout.write(
                    self.style.NOTICE(f'Found {inactive_users.count()} inactive users eligible for deletion.')
                )
                
                for user in inactive_users:
                    # Check if they already have a deletion request
                    existing_request = UserDataDeletionRequest.objects.filter(
                        user=user,
                        status__in=['requested', 'processing']
                    ).exists()
                    
                    if existing_request:
                        continue
                    
                    if dry_run:
                        self.stdout.write(
                            f'DRY RUN: Would create deletion request for inactive user {user.email}'
                        )
                    else:
                        # Create a deletion request for inactive users
                        deletion_request = UserDataDeletionRequest.objects.create(
                            user=user,
                            reason='Automatic deletion of inactive account'
                        )
                        deletion_request.schedule_deletion()
                        self.stdout.write(
                            self.style.SUCCESS(f'Created deletion request for inactive user {user.email}')
                        )
            else:
                self.stdout.write(
                    self.style.SUCCESS('No inactive users found for deletion.')
                )