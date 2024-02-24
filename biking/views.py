import json
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from biking.utils import importGPXFilesFromS3
from .models import Activity, GPSTrackpoint 
from django.core import serializers

# Create your views here.
def map_view(request, *args, **kwargs):
    activities = Activity.objects.all()
    output = []
    for activity in activities:
        output.append(activity.serialize())
    activities_json = json.dumps(output, default=str)
    # activities_json = serializers.serialize('json', activities)
    # print(activities_json)

    return render(request, "biking/map.html", { 'activities': activities_json })

# Post endpoint to import rides, returns 200 ok
def importRides(request):
    importGPXFilesFromS3()
    return HttpResponse(status=200)
