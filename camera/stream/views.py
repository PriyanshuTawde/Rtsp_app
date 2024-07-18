# Create
# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .models import RTSPStream
from .serializers import RTSPStreamSerializer
from rest_framework import status
import subprocess



class RTSPStreamCreateView(generics.CreateAPIView):
    queryset = RTSPStream.objects.all()
    serializer_class = RTSPStreamSerializer

    def perform_create(self, serializer):
        rtsp_input_url = serializer.validated_data['input_url']
        rtsp_server_url = "rtsp://localhost:8554"
        rtsp_output_url = f"{rtsp_server_url}/{hash(rtsp_input_url)}"

        # Start FFmpeg process for restreaming
        command = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',  # Use TCP for RTSP
            '-i', rtsp_input_url,  # Input URL
            '-c:v', 'copy',  # Copy the video codec
            '-f', 'rtsp',  # Output format
            rtsp_output_url  # Output URL 
        ]
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Save the output URL in the database
        serializer.save(output_url=rtsp_output_url)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        rtsp_stream = RTSPStream.objects.get(pk=response.data['id'])
        return Response({
            "id": rtsp_stream.id,
            "input_url": rtsp_stream.input_url,
            "output_url": rtsp_stream.output_url
        })







@api_view(['GET'])
def rtsp_stream_retrieve(request, id):
    try:
        stream = RTSPStream.objects.get(id=id)
    except RTSPStream.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RTSPStreamSerializer(stream)
    return Response(serializer.data)

@api_view(['PUT'])
def rtsp_stream_update(request, id):
    try:
        stream = RTSPStream.objects.get(id=id)
    except RTSPStream.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RTSPStreamSerializer(stream, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def rtsp_stream_delete(request, id):

    try:
        stream = RTSPStream.objects.get(id=id)
    except RTSPStream.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    stream.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['POST'])
def regenerate_output_url(request, id):
    try:
        stream = RTSPStream.objects.get(id=id)
    except RTSPStream.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    rtsp_input_url = stream.input_url
    rtsp_server_url = "rtsp://localhost:8554"
    new_rtsp_output_url = f"{rtsp_server_url}/{hash(rtsp_input_url)}"
 
    # Start FFmpeg process for the new output URL
    command = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',  # Use TCP for RTSP
        '-i', rtsp_input_url,  # Input URL
        '-c:v', 'copy',  # Copy the video codec
        '-f', 'rtsp',  # Output format
        new_rtsp_output_url  # New Output URL
    ]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Update the output URL in the database
    stream.output_url = new_rtsp_output_url
    stream.save()

    serializer = RTSPStreamSerializer(stream)
    return Response(serializer.data)