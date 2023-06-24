from django.contrib import admin
from .models import hospital_profiles

#admin.site.register(hospital_profiles)
class hospital_profile(admin.ModelAdmin):
    list_display = ['hospital_name','hospital_address','phone_number']
# Register your models here.
admin.site.register(hospital_profiles,hospital_profile)
