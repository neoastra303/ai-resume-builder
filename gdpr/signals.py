from django.db.models.signals import pre_delete
from django.dispatch import receiver
from resume_builder.models import User
from resumes.models import Resume


@receiver(pre_delete, sender=User)
def delete_user_data(sender, instance, **kwargs):
    """
    Delete all user data when a user is deleted
    """
    # Delete all resumes associated with the user
    Resume.objects.filter(user=instance).delete()