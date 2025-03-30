from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MilitaryProfile

@receiver(post_save, sender=User)
def create_military_profile(sender, instance, created, **kwargs):
    """Create a MilitaryProfile for each new User."""
    if created:
        MilitaryProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_military_profile(sender, instance, **kwargs):
    """Save the MilitaryProfile when the User is saved."""
    try:
        instance.militaryprofile.save()
    except MilitaryProfile.DoesNotExist:
        MilitaryProfile.objects.create(user=instance)