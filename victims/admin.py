from django.contrib import admin
from .models import All_profiles, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class AllProfileAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    readonly_fields = ('imgpreview',)

    def imgpreview(self, obj):
        return obj.imgpreview()

    imgpreview.short_description = 'Image Preview'
    imgpreview.allow_tags = True

admin.site.register(All_profiles, AllProfileAdmin)
