# from django.db import models

# Create your models here.
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Transcript(models.Model):
    meetIdURl = models.CharField(max_length=100)
    script = models.TextField()

    def __str__(self):
        return self.script
    

class Meet(models.Model):
    meetId = models.CharField(max_length=100)
    isRecording = models.BooleanField(default=True)
    
    def __str__(self):
        return self.meetId