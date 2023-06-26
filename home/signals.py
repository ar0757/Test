from django.db.models.signals import post_save
from django.dispatch import receiver
from timeline.models import TimelineEvent
from .models import home_profiles

@receiver(post_save, sender=home_profiles)
def create_home_profiles_timeline_event(sender, instance, created, **kwargs):
    if created:
        title = f"New home added: {instance.home_name}"
        description = f"Address: {instance.home_address}"
        event = TimelineEvent.objects.create(title=title, description=description)