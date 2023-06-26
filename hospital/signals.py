from django.db.models.signals import post_save
from django.dispatch import receiver
from timeline.models import TimelineEvent
from .models import hospital_profiles
@receiver(post_save, sender=hospital_profiles)
def create_hospital_profiles_timeline_event(sender, instance, created, **kwargs):
    if created:
        instance.create_timeline_event()
