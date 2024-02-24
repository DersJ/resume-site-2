import boto3
import resumesite2.settings as settings
from .models import Activity 

def importGPXFilesFromS3(): 
    session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')

    my_bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    for my_bucket_object in my_bucket.objects.filter(Prefix="rides/"):
        activity = Activity.objects.filter(file=my_bucket_object.key).first()
        if activity is None:
            activity = Activity(file=my_bucket_object.key)
            activity.save()