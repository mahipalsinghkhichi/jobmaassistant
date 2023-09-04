from django.urls import path
from .views import *

urlpatterns = [
    path('startRecording/', startRecording ),
    path('stopRecording/', stopRecording ),
    path('getTranscripts/', getTranscripts ),
    # path('startRecordingWithLastURlForTesting/', startRecordingWithLastURlForTesting ),
]
