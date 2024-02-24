from django.db import models
import gpxpy
import gpxpy.gpx

# Ride model
class Activity(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='rides/', blank=True)
    activityType = models.CharField(max_length=64, blank=True, null=True)

    def waypoints(self):
        return self.gpstrackpoint_set.all()

    def __str__(self):
        return f"{self.name} - {self.datetime}"
    
    def serialize(self):
        return {
            'name': self.name,
            'datetime': self.datetime,
            'distance': self.distance,
            'comment': self.comment,
            'activityType': self.activityType,
            'waypoints': [waypoint.serialize() for waypoint in self.waypoints()]
        }
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_file = Activity.objects.get(pk=self.pk).file
            if self.file != original_file:
                self.process_gpx_file()
                super().save(*args, **kwargs)
        else: 
            super().save(*args, **kwargs)
            self.process_gpx_file()
            super().save(*args, **kwargs)

    def process_gpx_file(self):
        if not self.file.name.endswith('.gpx'):
            raise ValueError("File is not a GPX file")
        
        self.gpstrackpoint_set.all().delete()
        
        gpx_file = self.file.read()
        gpx = gpxpy.parse(gpx_file)
        if not len(gpx.tracks):
            raise ValueError("GPX file contains no tracks")

        self.name = gpx.tracks[0].name
        self.activityType = gpx.tracks[0].type
        gpx.simplify(3)
        trackpoints = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if not self.datetime:
                        self.datetime = point.time
                    trackpoints.append(
                        GPSTrackpoint(
                            activity=self,
                            latitude=point.latitude,
                            longitude=point.longitude,
                            elevation=point.elevation,
                            datetime=point.time
                        )
                    )
        GPSTrackpoint.objects.bulk_create(trackpoints)
        

    
class GPSTrackpoint(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=11, decimal_places=7)
    longitude = models.DecimalField(max_digits=11, decimal_places=7)
    elevation = models.DecimalField(max_digits=6, decimal_places=2)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return f"{self.datetime} - {self.latitude}, {self.longitude}"
    
    def serialize(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'elevation': self.elevation,
            'datetime': self.datetime
        }
    
