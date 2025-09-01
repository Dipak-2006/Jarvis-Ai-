import os
import eel
import time
import threading
import platform
import webbrowser
import tkinter as tk
import pyttsx3
import pygame
import pyautogui
import requests
import speech_recognition as sr
import cv2
from PIL import Image, ImageTk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from gtts import gTTS
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import google.generativeai as genai
from PyDictionary import PyDictionary
dictionary = PyDictionary()


WEATHER_API_KEY = "b2e8f4ff51d93f378844ce06669c7373"
API_KEY = "AIzaSyD4EBLPp_OE-FAMTdVQLnkCzdGUcLiwHvo"
NEWS_API_KEY = "194ad47e83364f63838121301d981b61"
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

genai.configure(api_key=API_KEY)
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()
TEMP_AUDIO_FILE = "temp.mp3"

def speak(text):
    print(f"🗣️ Jarvis: {text}")
    try:
        eel.show_jarvis_response(text)  # GUI me dikhane ke liye
    except:
        pass

    try:
        tts = gTTS(text=text, lang='en')
        tts.save(TEMP_AUDIO_FILE)

        pygame.mixer.music.load(TEMP_AUDIO_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except:
            pass

        for _ in range(3):
            try:
                os.remove(TEMP_AUDIO_FILE)
                break
            except PermissionError:
                time.sleep(0.1)
    except Exception as e:
        print(f"gTTS failed: {e} — falling back to pyttsx3")
        engine.say(text)
        engine.runAndWait()



def get_user_city():
    try:
        ip_info = requests.get('https://ipapi.co/json').json()
        return ip_info.get("city", "Delhi")
    except:
        return "Delhi"

def get_weather():
    city = get_user_city()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={"b2e8f4ff51d93f378844ce06669c7373"}&units=metric&lang=hi"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"{city} के मौसम की जानकारी नहीं मिल पाई।"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f" तापमान {temp} डिग्री सेल्सियस है और मौसम {desc} है।"
    except:
        return "मौसम सर्वर से संपर्क नहीं हो पाया।"


def update_user_location():
    try:
        ip_info = requests.get('https://ipapi.co/json').json()
        city = ip_info.get("city", "Unknown")
        region = ip_info.get("region", "")
        country = ip_info.get("country_name", "")
        location = f"{city}, {region}, {country}"
        user_profile["location"] = location
        return location
    except:
        user_profile["location"] = "India"
        return "India"
    
def number_to_hindi(num):
    hindi_numbers = {
        0: "शून्य", 1: "एक", 2: "दो", 3: "तीन", 4: "चार", 5: "पांच",
        6: "छह", 7: "सात", 8: "आठ", 9: "नौ", 10: "दस", 11: "ग्यारह",
        12: "बारह", 13: "तेरह", 14: "चौदह", 15: "पंद्रह", 16: "सोलह",
        17: "सत्रह", 18: "अठारह", 19: "उन्नीस", 20: "बीस", 21: "इक्कीस",
        22: "बाईस", 23: "तेईस", 24: "चौबीस", 25: "पच्चीस", 26: "छब्बीस",
        27: "सत्ताईस", 28: "अट्ठाईस", 29: "उनतीस", 30: "तीस", 31: "इकतीस",
        32: "बत्तीस", 33: "तैंतीस", 34: "चौंतीस", 35: "पैंतीस", 36: "छत्तीस",
        37: "सैंतीस", 38: "अड़तीस", 39: "उनतालीस", 40: "चालीस", 41: "इकतालीस",
        42: "बयालीस", 43: "तैंतालीस", 44: "चवालीस", 45: "पैंतालीस", 46: "छयालिस",
        47: "सैंतालीस", 48: "अड़तालीस", 49: "उनचास", 50: "पचास", 51: "इक्यावन",
        52: "बावन", 53: "तिरेपन", 54: "चौवन", 55: "पचपन", 56: "छप्पन",
        57: "सत्तावन", 58: "अट्ठावन", 59: "उनसठ"
    }
    return hindi_numbers.get(num, str(num))


def get_time_in_hindi():
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min

    # Convert 24-hour to 12-hour
    if hour == 0:
        hour = 12
        ampm = "रात"
    elif hour < 12:
        ampm = "सुबह"
    elif hour == 12:
        ampm = "दोपहर"
    else:
        hour -= 12
        ampm = "शाम"

    hour_text = number_to_hindi(hour)
    minute_text = number_to_hindi(minute)

    if minute == 0:
        return f"{ampm} के {hour_text} बजे हैं"
    else:
        return f"{ampm} के {hour_text} बजकर {minute_text} मिनट हुए हैं"




user_profile = {
    "name": "Deepak Maurya",
    "age": 21,
    "profession": "Computer Science Student",
    "skills": ["Python", "AI", "Web Development"],
    "hobbies": ["Gaming", "Coding", "Listening Music"],
   "location": ["Varanasi , India"]

}

#IMAGE FOLER ME SAVE HOE
def ensure_snap_folder():
    folder_path = "snap"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def ai_process(command):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(command)
        return response.text.strip()
    except Exception as e:
        print(f"AI error: {e}")
        return "AI service is currently unavailable."

def open_application(app):
    speak(f"Opening {app}")
    os_name = platform.system()
    app = app.lower()
    try:
        if "chrome" in app:
            os.system("start chrome" if os_name == "Windows" else "google-chrome")
        elif "notepad" in app:
            os.system("notepad" if os_name == "Windows" else "gedit")
        elif "code" in app:
            os.system("code")
        else:
            speak("Application not configured.")
    except Exception as e:
        speak(f"Error opening app: {e}")

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        speak(f"Volume set to {level} percent")
    except Exception as e:
        speak(f"Volume adjustment failed: {e}")

def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent")
    except Exception as e:
        speak(f"Brightness adjustment failed: {e}")

def take_screenshot():
    folder = ensure_snap_folder()
    filename = os.path.join(folder, f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")


def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        speak("Webcam not available")
        return
    ret, frame = cam.read()
    if ret:
        folder = ensure_snap_folder()
        filename = os.path.join(folder, f"webcam_{int(time.time())}.png")
        cv2.imwrite(filename, frame)
        speak(f"Image saved as {filename}")
    cam.release()


def detect_faces():
    speak("Face detection started")
    root = tk.Tk()
    root.title("Face Detection")
    label = tk.Label(root)
    label.pack()

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    def update():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            label.imgtk = img
            label.configure(image=img)
        label.after(10, update)

    root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy(), speak("Face detection stopped")))
    update()
    root.mainloop()

def process_command(command):
    target = command.lower()

    if target.startswith("open"):
        try:
            file_name = target.replace("open", "").strip().lower()
            search_paths = [
                r"C:\\Users\\laptop-susgpd3r\\deepa\\Documents",
                r"C:\\Users\\laptop-susgpd3r\\deepa\\Desktop",
                r"C:\\Users\\laptop-susgpd3r\\deepa\\Downloads"
            ]
            found = False
            for folder in search_paths:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file_name in file.lower():
                            full_path = os.path.join(root, file)
                            os.startfile(full_path)
                            speak(f"Opening {file}")
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                speak(f"Koi file nahi mili jo '{file_name}' se match karti ho.")
        except Exception as e:
            speak(f"File open karte waqt error aaya. {e}")

def get_meaning(command):
    words = command.lower().replace("meaning of", "").replace("what is", "").strip()
    if not words:
        speak("Please provide the word or phrase you'd like the meaning of.")
        return
    meaning = dictionary.meaning(words)
    if meaning:
        first_def = next(iter(meaning.values()))[0]
        speak(f"The meaning of {words} is: {first_def}")
    else:
        speak(f"Sorry, I couldn't find the meaning of {words}.")


#------PROCESS COMMAND------------
def process_command(command):
    target = command.lower()

    if "meaning of" in target or target.startswith("what is"):
        get_meaning(command)

    # ...baaki command yahin handle karo...


def process_command(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "screenshot" in command:
      take_screenshot()
    
        
    elif "camera" in command or "capture image" in command:             #PHOOTUUUUUUUU
        capture_image()
    
    elif "face detection" in command:                                   #LIVE CHEHRAAAAAAAAAA
        threading.Thread(target=detect_faces, daemon=True).start()
   
    elif "who am i" in command or "about me" in command:                 #MERE  BAARE ME EEEE
        speak(f"You are {user_profile['name']}, a {user_profile['age']} year old {user_profile['profession']} from {user_profile['location']}.")
    


    elif "volume" in command:                         #AAWAZZZZZZZZZ
        if "mute" in command:
            set_volume(0)
        elif "increase" in command:
            set_volume(100)
        elif "decrease" in command:
            set_volume(50)
        elif "set volume to" in command:
            try:
                level = int(''.join(filter(str.isdigit, command)))
                set_volume(level)
            except:
                speak("Invalid volume level")
    
    elif "brightness" in command:                         #ROSHNIIIIIIIIIIIIIII
        if "set brightness to" in command:
            try:
                level = int(''.join(filter(str.isdigit, command)))
                set_brightness(level)
            except:
                speak("Invalid brightness level")
        elif "increase" in command:
            set_brightness(100)
        elif "decrease" in command:
            set_brightness(50)
    elif "news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={"194ad47e83364f63838121301d981b61"}")
            articles = r.json().get('articles', [])[:5]
            for article in articles:
                speak(article.get('title', ''))
        except:
            speak("Unable to fetch news")
    else:
        response = ai_process(command)
        speak(response)

if __name__ == "__main__":
    speak("Hello Sir...")

    # hindi_time = get_time_in_hindi()
    # speak(f"वर्तमान समय {hindi_time}")

    # # 🌦️ Get Weather
    # weather = get_weather()
    # speak(weather)
   
# 🌐 Initialize GUI (HTML, CSS, JS inside 'web' folder)
eel.init('web')


# 🗣️ Speak function (placeholder)
# def speak(text):
#     print(f"🗣️ Jarvis: {text}")
#     eel.show_jarvis_response(text)  # GUI pe dikhane ke liye



# 🎧 Listen after wake word
def listen_after_wake():
    recognizer = sr.Recognizer()
    wake_word_heard = False

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)

                if not wake_word_heard:
                    print("🎧 Waiting for wake word: 'wake up'")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    try:
                        wake_word = recognizer.recognize_google(audio).lower()
                        print(f"🔊 Heard: {wake_word}")
                        if "friday" in wake_word or "edith" in wake_word or"wake up" in wake_word or "hello" in wake_word:
                            speak("Yes sir")
                            wake_word_heard = True
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        speak(f"Speech service error: {e}")
                else:
                    print("🎧 Jarvis is now listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                    try:
                        command = recognizer.recognize_google(audio).lower()
                        print(f"📢 You said: {command}")
                        process_command(command)
                    except sr.UnknownValueError:
                        print("🤔 Didn't catch that.")
                    except sr.RequestError as e:
                        speak(f"API error: {e}")
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            speak(f"⚠️ Error occurred: {e}")


# 🧠 GUI se command lene ka exposed function
@eel.expose
def get_jarvis_response(command):
    print(f"🎧 Command received from GUI: {command}")
    threading.Thread(target=process_command, args=(command,), daemon=True).start()
    return f"Processing your command: {command}"


# 🌟 GUI open hote hi wake listener background mein chalu karo
def start_jarvis():
    threading.Thread(target=listen_after_wake, daemon=True).start()


# 🚀 Start the GUI
eel.start("jarvis_gui.html", size=(600, 600), block=False)

# 🕓 Delay to ensure GUI is open first
time.sleep(1)

# 🎙️ Then start background listener
start_jarvis()

# 🌀 Keep the app running
while True:
    eel.sleep(1)
