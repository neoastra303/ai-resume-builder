from django.core.management.base import BaseCommand
from django.utils import timezone
from django_otp.plugins.otp_totp.models import TOTPDevice
from datetime import timedelta


class Command(BaseCommand):
    help = 'Clean up unconfirmed 2FA devices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Delete unconfirmed devices older than specified days (default: 7)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Find unconfirmed TOTP devices older than cutoff date
        unconfirmed_devices = TOTPDevice.objects.filter(
            confirmed=False,
            created_at__lte=cutoff_date
        )
        
        count = unconfirmed_devices.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No unconfirmed 2FA devices found for cleanup.')
            )
            return
        
        self.stdout.write(
            self.style.NOTICE(f'Found {count} unconfirmed 2FA devices older than {days} days.')
        )
        
        # Confirm deletion
        confirm = input('Do you want to delete these devices? (yes/no): ')
        if confirm.lower() != 'yes':
            self.stdout.write('Cleanup cancelled.')
            return
        
        # Delete unconfirmed devices
        deleted_count, _ = unconfirmed_devices.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} unconfirmed 2FA devices.')
        )