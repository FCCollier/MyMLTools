from django.db import models


# Create your models here.
class Actress(models.Model):
    actress_name = models.CharField(max_length=200)


class Video(models.Model):
    video_title=models.CharField(max_length=200)
    actress_name=models.ForeignKey(Actress,on_delete=models.CASCADE)
