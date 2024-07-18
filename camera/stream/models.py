# myapp/models.py
from django.db import models

class RTSPStream(models.Model):
    input_url = models.CharField(max_length=255)
    output_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.input_url
