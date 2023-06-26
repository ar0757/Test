from django.db import models
import shortuuid
from timeline.models import TimelineEvent
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class home_profiles(models.Model):
    CATEGORY_LISTS = (
        ('CORPORATION', 'CORPORATION'),
        ('PRIVATE', 'PRIVATE'),
        ('OTHER', 'OTHER')
    )
    id = models.CharField(max_length=22, primary_key=True, default=shortuuid.uuid, editable=False)
    home_name = models.CharField(max_length=50)
    home_address = models.CharField(max_length=200)
    phone_number = models.IntegerField(default=0)
    contact_person = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_LISTS)
    beds = models.IntegerField(default=0)

    class Meta:
        verbose_name = "home"

    def __str__(self):
        return f"{self.home_name},{self.home_address},{self.phone_number},{self.contact_person},{self.category},{self.beds}"
    
    def create_timeline_event(self):
        title = f"New home added: {self.home_name}"
        description = f"Address: {self.home_address}"
        event = TimelineEvent.objects.create(title=title, description=description)
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.create_timeline_event()

   


