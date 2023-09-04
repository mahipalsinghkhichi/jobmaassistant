import pyaudio
import wave
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.command import Command

import time
import sqlite3
import speech_recognition as sr

def transcribe_audio(frames, meetURL, conn):
    recognizer = sr.Recognizer()
    audio_data = b''.join(frames)
    try:
        with wave.open(f"recorded_audio_chunk.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(44100)
            wf.writeframes(audio_data)

        # Convert the audio to text using the 'transcript' library
        audio_path = f"recorded_audio_chunk.wav"
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(f"Transcription:\n{text}")

        cur = conn.cursor()
        # Use placeholders in your SQL query
        sql = "INSERT INTO myapp_transcript (meetIdURl, script) VALUES (?, ?)"
        cur.execute(sql, (meetURL, text))
        conn.commit()

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def isdriverRunning(driver):
    try:
        pageTitle = driver.title
        return True
    except:
        return False

def fillName(driver):
    try:
        # Ask to Join meet
        time.sleep(0.5)
        driver.implicitly_wait(2000)
        input_element = driver.find_element(By.XPATH, '/html/body/div/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[1]/div[3]/label/input')

        # Clear the input field (optional, if you want to clear it first)
        input_element.clear()

        # Send keys to the input field to fill it
        input_element.send_keys("Jobma.AI")
        return True
    except Exception as e:
        print("Name fill not working..  ", e)
        return False


def AskToJoin(driver):
    try:
        # Ask to Join meet
        time.sleep(0.5)
        driver.implicitly_wait(2000)
        driver.find_element(By.XPATH,
            '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button').click()
        return True
    except Exception as e:
        print("Ask to join not working...  ", e)
        return False
    
# explicit function to turn off mic and cam
def turnOffMicCam(driver):
    try:
        # turn off Microphone
        time.sleep(0.5)
        driver.find_element(By.XPATH,
            '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[1]/div/div/div[1]').click()
        driver.implicitly_wait(3000)
    
        # turn off camera
        time.sleep(0.5)
        driver.find_element(By.XPATH,
            '//*[@id="yDmH0d"]/c-wiz/div/div/div[14]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[5]/div[2]/div/div[1]').click()
        driver.implicitly_wait(3000)
        return True
    except:
        print("No able to turn off camera and mic.")
        return False


def create_connection():
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect("./../myproject/db.sqlite3")
    except Exception as e:
        print(e)
    return conn

def getmeetingUrl(conn, id):
    cur = conn.cursor()
    cur.execute(f"select meetId from myapp_meet where id={id};")
    data = cur.fetchall()
    if data and len(data)>0 and len(data[0])>0:
        return data[0][0]
    else:
        return None

def createDriver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow audio capture
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option("prefs", {
    
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1
    })
    # Path to ChromeDriver executable
    chromedriver_path = "addingBot/chromedriver.exe"
    # Initialize Chrome Service
    chrome_service = Service(executable_path=chromedriver_path)
    # Initialize WebDriver
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def JointTheMeetAndGetInstanceId(driver, connection, instanceId):
    if connection:
        meetUrl = getmeetingUrl(connection, instanceId)
        if meetUrl:
            driver.get(meetUrl)
            return meetUrl
        
def isStillRecording(conn, id):
    cur = conn.cursor()
    cur.execute(f"select isRecording from myapp_meet where id={id};")
    data = cur.fetchall()
    if data and len(data)>0 and len(data[0])>0:
        return bool(data[0][0])
    else:
        return False

def startRecording(driver, conn, instanceId, meetURL):

    # Wait for the content to load (adjust time as needed)
    time.sleep(5)
    working = turnOffMicCam(driver)
    if not working:
        return
    working = fillName(driver)
    if not working:
        return
    working = AskToJoin(driver)
    if not working:
        return

    if isdriverRunning(driver):
        # Initialize audio recording
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

        # Start recording
        frames = []
        fiveSecFrames = []
        isRecroding = isdriverRunning(driver)

        while isRecroding:
            data = stream.read(1024)
            frames.append(data)
            fiveSecFrames.append(data)
            if len(fiveSecFrames) >= 500:  # 44100 samples per second * 2 channels * 3 seconds
                transcribe_audio(fiveSecFrames, meetURL, conn)
                fiveSecFrames = []
                
            isRecroding = isStillRecording(conn, instanceId) and isdriverRunning(driver)

        # Stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a WAV file
        with wave.open(f"recorded_audio_{instanceId}.wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))

        # Clean up and close the browser
        driver.quit()

def main(instanceId):
    driver = createDriver()
    conn = create_connection()
    meetURL = JointTheMeetAndGetInstanceId(driver, conn, instanceId)
    if instanceId:
        startRecording(driver, conn, instanceId, meetURL)