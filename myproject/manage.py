#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# import pyaudio
# import wave
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.command import Command

# import time



# # Set up Chrome options
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
# chromedriver_path = "C:/Users/User/Desktop/jobmaassistant/Adding-bot/chromedriver.exe"

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
#         # Ask to Join meet
#         time.sleep(5)
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
#         time.sleep(5)
#         driver.implicitly_wait(2000)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button').click()
#     except Exception as e:
#         print("Ask to join not working...  ", e)
    
# # explicit function to turn off mic and cam
# def turnOffMicCam():
#     try:
#         # turn off Microphone
#         time.sleep(2)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[1]/div/div/div[1]').click()
#         driver.implicitly_wait(3000)
    
#         # turn off camera
#         time.sleep(1)
#         driver.find_element(By.XPATH,
#             '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[2]/div/div[1]').click()
#         driver.implicitly_wait(3000)
#     except:
#         print("No able to turn off camera and mic.")


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

# # Initialize audio recording
# audio = pyaudio.PyAudio()
# stream = audio.open(format=pyaudio.paInt16,
#                     channels=2,
#                     rate=44100,
#                     input=True,
#                     frames_per_buffer=1024)

# # Start recording
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

# # http://localhost:5000/start-recording