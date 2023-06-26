from django.db.models.signals import post_save
from django.dispatch import receiver
from timeline.models import TimelineEvent
from .models import volunteer_profiles

@receiver(post_save, sender=volunteer_profiles)
def create_volunteer_profiles_timeline_event(sender, instance, created, **kwargs):
    if created:
        instance.create_timeline_event()