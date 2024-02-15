from django.db import models
import shortuuid
from timeline.models import TimelineEvent
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class hospital_profiles(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=shortuuid.uuid, editable=False)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.CharField(max_length=300)
    phone_number = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Hospital Profile"

    def __str__(self):
        return f"{self.hospital_name},{self.hospital_address},{self.phone_number}"
    
    def create_timeline_event(self):
        title = f"New hospital added: {self.hospital_name}"
        description = f"Address: {self.hospital_address}"
        event = TimelineEvent.objects.create(title=title, description=description,user = self.user)
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.create_timeline_event()

