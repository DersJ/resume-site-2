from django.contrib import admin

from biking.utils import importGPXFilesFromS3

# Register your models here.
from .models import Activity, GPSTrackpoint

@admin.action(description="Import rides from S3")
def import_rides(modeladmin, request, queryset):
    importGPXFilesFromS3()

@admin.register(Activity)
class ActivityModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "file"]
    actions = [import_rides]
    class Meta:
        model = Activity
    



admin.site.register(GPSTrackpoint)