import pyaudio
import wave 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
import time
from django.http import JsonResponse
# from .tasks import start_bot_recording
from addingBot.main import main

from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Meet, Transcript
# from .serializers import ItemSerializer

import threading

# Create a global variable to hold the reference to the thread running your program
my_program_thread = None


@api_view(['POST'])
def startRecording(request):

    meetIdUrl = request.data["meetIdUrl"]
    meet = Meet.objects.create(meetId=meetIdUrl)
    meet.save()
    # start_bot_recording.delay(meet.id)
    
    global my_program_thread
    def my_continuous_program():
            main(meet.id)

    if my_program_thread is None or not my_program_thread.is_alive():
        # Start the program in a new thread
        my_program_thread = threading.Thread(target=my_continuous_program)
        my_program_thread.start()

        return Response({'status': 'Started', "id": meet.id})
    
    return Response({'status': 'failed', "id": meet.id})


@api_view(['POST'])
def stopRecording(request):

    meetIdUrl = request.data["meetIdUrl"]
    meet = Meet.objects.filter(meetId=meetIdUrl).last()
    if meet:
        meet.isRecording = False
        meet.save()
    return Response({'status': 'success', "id": meet.id})


@api_view(['POST'])
def getTranscripts(request):
    meetIdUrl = request.data["meetIdUrl"]
    lastTCId = int(request.data["lastTCId"])

    # Filter transcripts to get only new ones
    transcripts = Transcript.objects.filter(id__gt=lastTCId, meetIdUrl=meetIdUrl)

    if not transcripts.exists():
        return Response({'status': 'failed'})

    data = []
    for trans in transcripts.all():
        data.append({
            'tcId': trans.id,  # Include the transcript ID in the response
            'script': trans.script
        })

    newLastId = transcripts.last().id
    return Response({'status': 'success', "lastTCId": newLastId, "transcripts": data })



# @api_view(['GET'])
# def startRecordingWithLastURlForTesting(request):
#     global my_program_thread

#     meet = Meet.objects.all().last()
#     if meet:

#         def my_continuous_program():
#             main(meet.id)
#         # start_bot_recording.delay(meet.id)

#         if my_program_thread is None or not my_program_thread.is_alive():
#             # Start the program in a new thread
#             my_program_thread = threading.Thread(target=my_continuous_program)
#             my_program_thread.start()
#             return Response({'status': 'Started', "id": meet.id})

#     return Response({"status": "Already running"})




# chrome_options = Options()
# chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow audio capture
# chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_argument('--start-maximized')
# chrome_options.add_experimental_option("prefs", {

#     "profile.default_content_setting_values.media_stream_mic": 1,
#     "profile.default_content_setting_values.media_stream_camera": 1,
#     "profile.default_content_setting_values.geolocation": 0,
#     "profile.default_content_setting_values.notifications": 1
# })

# # Path to ChromeDriver executable
# chromedriver_path = "D:\jobmaassistant\Adding-bot\chromedriver.exe"

# # Initialize Chrome Service
# chrome_service = Service(executable_path=chromedriver_path)

# # Initialize WebDriver
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)



# def isDeriverRunning():
#     try:
#         print(driver.title)
#         return True
#     except:
#         return False

# def fillName():
#     try:
#         time.sleep(2)
#         driver.implicitly_wait(2000)
#         input_element = driver.find_element(By.XPATH, '//*[@id="c15"]')

#         # Clear the input field (optional, if you want to clear it first)
#         input_element.clear()

#         # Send keys to the input field to fill it
#         input_element.send_keys("Mahipal's bot")
#     except Exception as e:
#         print("Name fill not working..  ", e)



# def AskToJoin():
#     try:
#         # Ask to Join meet
#         time.sleep(2)
#         driver.implicitly_wait(2000)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button').click()
#     except Exception as e:
#         print("Ask to join not working...  ", e)


# # explicit function to turn off mic and cam
# def turnOffMicCam():
#     try:
#         # turn off Microphone
#         time.sleep(1)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[1]/div/div/div[1]').click()
#         driver.implicitly_wait(1000)
    
#         # turn off camera
#         time.sleep(1)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[2]/div/div[1]').click()
#         driver.implicitly_wait(1000)
#     except:
#         print("No able to turn off camera and mic.")

    

# @api_view(['POST'])
# def api_root(request):

#     meetId = request.data["meetId"]
#     meet = Meet.objects.create(meetId=meetId)
#     meet.save()
#     # data = {'key': 'value'}
#     # return JsonResponse(data)
#     print(request.data.get("meetId"),"***********************************")
#     # url = "https://meet.google.com/qsr-aaxo-bbo"
#     # url = request.data.get("meetId")
#     # driver.get(url)
#     # print(driver,">>>>>>>>>>>>>>>>>>>>>>>>>")
#     # # time.sleep(5)
#     # turnOffMicCam()
#     # fillName()
#     # # time.sleep(1)
#     # AskToJoin()
#     # isDeriverRunning()
        
#     # # Initialize audio recording
#     # audio = pyaudio.PyAudio()
#     # stream = audio.open(format=pyaudio.paInt16,
#     #                     channels=2,
#     #                     rate=44100,
#     #                     input=True,
#     #                     frames_per_buffer=1024)

#     # #Start recording
#     # frames = []
#     # isRecroding = True

#     # while isRecroding:
#     #     data = stream.read(1024)
#     #     frames.append(data)

#     #     isRecroding = isDeriverRunning()

#     # # Stop recording
#     # stream.stop_stream()
#     # stream.close()
#     # audio.terminate()

#     # # Save the recorded audio to a WAV file
#     # with wave.open("recorded_audio.wav", "wb") as wf:
#     #     wf.setnchannels(2)
#     #     wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
#     #     wf.setframerate(44100)
#     #     wf.writeframes(b''.join(frames))
#     # # Clean up and close the browser
#     # driver.quit()

#     import os
#     os.system('python cout.py '+f'{meet.id}')
#     return Response({'status': 'success', "id": meet.id})

# # Open Google Meet or YouTube video URL
# # url = "https://www.youtube.com/watch?v=VGhw7ps25ig"
# url = "https://meet.google.com/ktz-sprh-ezd"
# driver.get(url)

# # Wait for the content to load (adjust time as needed)
# time.sleep(5)
# turnOffMicCam()
# fillName()
# time.sleep(1)
# AskToJoin()

# isDeriverRunning()

# Initialize audio recording
# audio = pyaudio.PyAudio()
# stream = audio.open(format=pyaudio.paInt16,
#                     channels=2,
#                     rate=44100,
#                     input=True,
#                     frames_per_buffer=1024)

# #Start recording
# frames = []
# isRecroding = True

# while isRecroding:
#     data = stream.read(1024)
#     frames.append(data)

#     isRecroding = isDeriverRunning()

# # Stop recording
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Save the recorded audio to a WAV file
# with wave.open("recorded_audio.wav", "wb") as wf:
#     wf.setnchannels(2)
#     wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
#     wf.setframerate(44100)
#     wf.writeframes(b''.join(frames))
# # Clean up and close the browser
# driver.quit()

# http://localhost:5000/start-recording