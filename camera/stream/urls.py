# myapp/urls.py
from django.urls import path
from .views import * #RTSPStreamCreateView #, ItemListView, ItemDetailView, ItemUpdateView, ItemDeleteView

urlpatterns = [
    path('streams/create/', RTSPStreamCreateView.as_view(), name='stream-create'),
    path('streams/<int:id>/', rtsp_stream_retrieve, name='stream-retrieve'),
    path('streams/<int:id>/update/', rtsp_stream_update, name='stream-update'),
    path('streams/<int:id>/delete/', rtsp_stream_delete, name='stream-delete'),
    path('streams/<int:id>/regenerate/', regenerate_output_url, name='regenerate_output_url'),
 
]
