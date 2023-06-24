from django.db import models
from django.utils.html import mark_safe
import shortuuid
from home.models import home_profiles
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
    Image = models.ImageField(upload_to="victims/images",default="")

    class Meta:
        verbose_name = "All Profile"

    def __str__(self):
        return f"{self.memo_no},{self.pickup_location}"

    def imgpreview(self):
        return mark_safe(f'<img src = "{self.Image.url}" width = "300"/>')