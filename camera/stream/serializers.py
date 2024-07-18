# myapp/serializers.py
from rest_framework import serializers
from .models import RTSPStream

class RTSPStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RTSPStream
        fields = ['id', 'input_url', 'output_url']
