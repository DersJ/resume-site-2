import json
from django.http import HttpResponse
from django.shortcuts import render

from biking.utils import importGPXFilesFromS3
from .models import Activity 

# Create your views here.
def map_view(request, *args, **kwargs):
    return render(request, "biking/map.html")

def activity_data(request):
    activities = Activity.objects.all()
    output = []
    for activity in activities:
        if activity.isInNC():
            output.append(activity.serialize())
    activities_json = json.dumps(output, default=str)
    return HttpResponse(activities_json, content_type="application/json")

# Post endpoint to import rides, returns 200 ok
def importRides(request):
    importGPXFilesFromS3()
    return HttpResponse(status=200)
