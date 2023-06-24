from django.db import models
import shortuuid


# Create your models here.
class hospital_profiles(models.Model):
    id = models.CharField(max_length=22, primary_key=True, default=shortuuid.uuid, editable=False)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.CharField(max_length=300)
    phone_number = models.IntegerField(default=0)


    class Meta:
        verbose_name = "Hospital Profile"

    def __str__(self):
        return f"{self.hospital_name},{self.hospital_address},{self.phone_number}"