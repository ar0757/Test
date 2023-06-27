from django.db import models
from django.utils.html import mark_safe
import shortuuid
from home.models import home_profiles
from django.contrib import admin
from timeline.models import TimelineEvent
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class All_profiles(models.Model):
    GENDER_LISTS=(
        ('MALE','MALE'),
        ('FEMALE','FEMALE'),
        ('OTHER','OTHER')
    )
    def name_choices():
        return [(a.home_name, a.home_name) for a in home_profiles.objects.all()]
    id = models.CharField(max_length=22, primary_key=True, default=shortuuid.uuid, editable=False)
    memo_no = models.IntegerField(default="",blank =True,null=True)
    first_name = models.CharField(max_length=50,default="",blank=True)
    last_name = models.CharField(max_length=50, default="", blank=True)
    age = models.IntegerField(default="",blank=True,null=True)
    gender = models.CharField(max_length=20,choices=GENDER_LISTS,blank=True)
    ngo_assigned = models.CharField(choices=name_choices(),default="",blank=True,max_length=100)
    description = models.CharField(max_length=1000)
    pickup_location = models.CharField(max_length=1000)
    pickup_date = models.DateTimeField()
    images = models.ManyToManyField('Image', related_name='victims')

    class Meta:
        verbose_name = "All Profile"

    def __str__(self):
        return f"{self.memo_no},{self.pickup_location}"
    
    def create_timeline_event(self):
        title = f"New victim added: {self.id}"
        descriptionn = f"Description: {self.description}\n"
        descriptionn += f"Pickup Date: {self.pickup_date}"
        event = TimelineEvent.objects.create(title=title, description=descriptionn)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.create_timeline_event()

class Image(models.Model):
    all_profile = models.ForeignKey(All_profiles, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="victims/images")

    def __str__(self):
        return self.image.name


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@receiver(post_save, sender=All_profiles)
def create_All_profiles_timeline_event(sender, instance, created, **kwargs):
    if created:
        instance.create_timeline_event()    

def protect_home_profiles_delete(sender, instance, **kwargs):
    if All_profiles.objects.filter(ngo_assigned=instance.home_name).exists():
        raise models.ProtectedError(
            "Cannot delete home_profiles object as it is referenced by All_profiles instances.",
            instance=instance,
        )