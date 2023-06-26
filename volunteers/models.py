from django.db import models
import shortuuid
from timeline.models import TimelineEvent
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class volunteer_profiles(models.Model):
    GENDER_LISTS=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    id = models.CharField(max_length=22, primary_key=True, default=shortuuid.uuid, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=20,choices=GENDER_LISTS)
    phone_number = models.IntegerField(default=0)
    ngo_association = models.CharField(max_length=100)
    area_of_operation = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Volunteer Profile"
    
    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.phone_number}"
    
    def create_timeline_event(self):
        title = f"New Volunteer added: {self.first_name} {self.last_name}"
        description = f"Phone No: {self.phone_number}\n"
        event = TimelineEvent.objects.create(title=title, description=description)
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.create_timeline_event()

