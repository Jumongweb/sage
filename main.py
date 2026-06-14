import datetime
import time
import webbrowser

import pyttsx3
import speech_recognition as sr
import platform
import subprocess
import shutil
import os
import pyautogui
import pvporcupine
import pyaudio
import struct

def initialize_speech_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    selected_voice = None

    # Try to find an American English voice
    for voice in voices:
        voice_name = voice.name.lower()
        voice_id = voice.id.lower()

        # Common American English voices:
        # Windows: Microsoft Zira, Microsoft David
        # macOS: Samantha, Alex
        if (
            "zira" in voice_name
            or "david" in voice_name
            or "samantha" in voice_name
            or "alex" in voice_name
            or "united states" in voice_name
            or "en-us" in voice_id
            or "en_us" in voice_id
        ):
            selected_voice = voice.id
            break

    # Fallback voice if no American English voice is found
    if selected_voice:
        engine.setProperty("voice", selected_voice)
    elif len(voices) > 1:
        engine.setProperty("voice", voices[1].id)
    else:
        engine.setProperty("voice", voices[0].id)

    # Make speech sound a bit more natural
    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate - 40)

    volume = engine.getProperty("volume")
    engine.setProperty("volume", min(volume + 0.25, 1.0))

    return engine


def speak_text(text):
    engine = initialize_speech_engine()
    engine.say(text)
    engine.runAndWait()

def open_text_editor(path: str | None = None, preferred: str | None = None) -> bool:
    """Open a text editor cross-platform.

    On Windows this opens Notepad. On macOS this opens TextEdit. On Linux
    it will try common editors (`gedit`, `xdg-open`, `nano`). Returns True
    if a command to open an editor was issued, False otherwise.
    """
    system = platform.system()
    try:
        if system == "Windows":
            # prefer explicit notepad when requested
            subprocess.Popen(["notepad"])
        elif system == "Darwin":
            # Allow opening Notes when preferred='notes', otherwise TextEdit
            if preferred and str(preferred).lower() == "notes":
                subprocess.Popen(["open", "-a", "Notes"])
            else:
                if path:
                    subprocess.Popen(["open", "-a", "TextEdit", path])
                else:
                    subprocess.Popen(["open", "-a", "TextEdit"])
        else:
            # Linux / other
            gedit = shutil.which("gedit")
            xdg = shutil.which("xdg-open")
            nano = shutil.which("nano")
            if gedit:
                subprocess.Popen([gedit, path or ""]) 
            elif xdg:
                subprocess.Popen([xdg, path or "."]) 
            elif nano:
                # try to open a terminal-based editor in a new terminal if possible
                term = shutil.which("x-terminal-emulator") or shutil.which("gnome-terminal") or shutil.which("konsole")
                if term:
                    subprocess.Popen([term, "-e", nano, path or ""]) 
                else:
                    subprocess.Popen([nano, path or ""]) 
        return True
    except Exception as e:
        print(f"Failed to open editor: {e}")
        return False

def close_text_editor(preferred: str | None = None) -> bool:
    """Close an editor/application cross-platform.

    On macOS, sends an AppleScript command to quit Notes or TextEdit.
    On Windows, uses taskkill to stop Notepad. On Linux, attempts pkill.
    """
    system = platform.system()
    try:
        if system == "Darwin":
            if preferred and str(preferred).lower() == "notes":
                subprocess.Popen(["osascript", "-e", 'tell application "Notes" to quit'])
            else:
                subprocess.Popen(["osascript", "-e", 'tell application "TextEdit" to quit'])
        elif system == "Windows":
            # best-effort to quit Notepad
            if preferred and str(preferred).lower() in ("notes", "notepad"):
                subprocess.Popen(["taskkill", "/IM", "notepad.exe", "/F"])
            else:
                subprocess.Popen(["taskkill", "/F", "/IM", "notepad.exe"])
        else:
            # Linux/other: try to kill common GUI editors
            if preferred and str(preferred).lower() in ("notes", "gedit"):
                subprocess.Popen(["pkill", "-f", "gedit"])
            else:
                subprocess.Popen(["pkill", "-f", "gedit"])
        return True
    except Exception as e:
        print(f"Failed to close editor: {e}")
        return False


def listen_for_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)

        print("Listening...", end="", flush=True)

        r.pause_threshold = 0.8
        r.non_speaking_duration = 0.5
        r.dynamic_energy_threshold = True
        r.dynamic_energy_adjustment_damping = 0.15
        r.energy_threshold = 300

        try:
            audio = r.listen(source, phrase_time_limit=10)
        except Exception as e:
            print(f"\nListening error: {e}")
            return None

    try:
        print("\rRecognizing...", end="", flush=True)

        # American English recognition
        text = r.recognize_google(audio, language="en-us")

        print(f"\nYou said: {text}")
        return text

    except sr.UnknownValueError:
        print("\nSorry, I did not understand that.")
        return None

    except sr.RequestError:
        print("\nSorry, my speech service is down.")
        return None


def cal_day():
    day = datetime.datetime.today().weekday() + 1

    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }

    day_of_week = day_dict.get(day, "Unknown")
    print(f"Today is: {day_of_week}")

    return day_of_week


def wish_me():
    hour = datetime.datetime.now().hour
    current_time = time.strftime("%I:%M %p")
    day = cal_day()

    if 0 <= hour < 12:
        speak_text(f"Good morning, Codefather. Today is {day}, and it's {current_time}.")
    elif 12 <= hour < 16:
        speak_text(f"Good afternoon, Codefather. Today is {day}, and it's {current_time}.")
    else:
        speak_text(f"Good evening, Codefather. Today is {day}, and it's {current_time}.")


def show_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    for index, voice in enumerate(voices):
        print(f"Voice {index}")
        print(f"Name: {voice.name}")
        print(f"ID: {voice.id}")
        print(f"Languages: {voice.languages}")
        print("-" * 40)


def social_media(command):
    if "facebook" in command:
        speak_text("Sure, opening Facebook for you.")
        webbrowser.open("https://www.facebook.com")
        # Add code to open Facebook
    elif "instagram" in command:
        speak_text("Opening Instagram now.")
        webbrowser.open("https://www.instagram.com")
        # Add code to open Instagram
    elif "twitter" in command:
        speak_text("Let me open Twitter for you.")
        webbrowser.open("https://www.twitter.com")
        # Add code to open Twitter
    elif "linkedin" in command:
        speak_text("Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")
    elif "github" in command:
        speak_text("Opening GitHub.")
        webbrowser.open("https://www.github.com")
        
    else:
        speak_text("Sorry, I can't access that platform right now.")

def schedule():
    day = cal_day().lower()
    speak_text("Let me check today's schedule for you.")
    week={
        "monday": "You have a meeting at 10 AM and a project deadline at 3 PM.",
        "tuesday": "You have a team lunch at 12 PM and a client call at 4 PM.",
        "wednesday": "You have a workshop at 2 PM and a code review at 5 PM.",
        "thursday": "You have a presentation at 11 AM and a team meeting at 3 PM.",
        "friday": "You have a brainstorming session at 1 PM and a project update at 4 PM.",
        "saturday": "You have a personal development session at 10 AM and a team outing at 2 PM.",
        "sunday": "You have a family gathering at 1 PM and some relaxation time at 5 PM.",
    }
    if day in week.keys():
        speak_text(week[day])

def wait_for_wake_word():
    """
    Listen for the wake word 'Hey Sage' using Porcupine.
    Returns True when wake word is detected.
    """
    porcupine = None
    pa = None
    audio_stream = None
    
    try:
        # Initialize Porcupine with the built-in 'hey siri' wake word (closest to "Hey Sage")
        # Note: For custom "Hey Sage" wake word, you'll need to train it at console.picovoice.ai
        porcupine = pvporcupine.create(keywords=['hey siri'])  # Using built-in, change to custom .ppn for "Hey Sage"
        
        pa = pyaudio.PyAudio()
        
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("Listening for wake word 'Hey Sage'...")
        
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("Wake word detected!")
                return True
                
    except Exception as e:
        print(f"Error in wake word detection: {e}")
        return False
    
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    # Uncomment this line if you want to see all available voices on your computer
    # show_available_voices()

    wish_me()

    while True:
        # Wait for wake word before listening to commands
        wake_word_detected = wait_for_wake_word()
        
        if not wake_word_detected:
            continue
        
        # Acknowledge wake word detection
        speak_text("Yes, Codefather?")
        
        result = listen_for_command()

        if not result:
            continue

        user_command = result.lower()

        if ('facebook' in user_command or 'instagram' in user_command or 'twitter' in user_command or 'linkedin' in user_command):
            social_media(user_command)

            # speak_text("Sorry Codefather, I cannot access social media platforms at the moment.")
            # continue

        if "exit" in user_command or "quit" in user_command or "stop" in user_command:
            speak_text("Goodbye, Codefather. Have a great day!")
            break

        print(f"User Command: {user_command}")

        # handle quick built-in actions: close requests first
        if any(kw in user_command for kw in ("close whatsapp", "quit whatsapp", "close whats app", "quit whats app")):
            speak_text("Closing WhatsApp now.")
            try:
                subprocess.run(['osascript', '-e', 'tell application "WhatsApp" to quit'])
                print("WhatsApp closed.")
            except Exception as e:
                print(f"Failed to close WhatsApp: {e}")
            continue

        if any(kw in user_command for kw in ("close notes", "close note", "quit notes", "quit note", "close editor", "close notepad")):
            if "note" in user_command or "notes" in user_command:
                speak_text("Closing Notes.")
                closed = close_text_editor(preferred="notes")
            else:
                speak_text("Closing the editor.")
                closed = close_text_editor()
            if closed:
                print("Editor closed.")
            else:
                print("Failed to close editor.")
            continue

        # open requests
        if any(kw in user_command for kw in ("open whatsapp", "open whats app", "launch whatsapp", "launch whats app")):
            speak_text("Opening WhatsApp for you.")
            try:
                subprocess.run(['open', '-a', 'WhatsApp'])
                print("WhatsApp opened.")
            except Exception as e:
                print(f"Failed to open WhatsApp: {e}")
            continue

        if any(kw in user_command for kw in ("open notepad", "open textedit", "open text edit", "open editor", "open code editor", "open notes", "open note")):
            if "note" in user_command or "notes" in user_command or "notepad" in user_command:
                speak_text("Opening Notes.")
                opened = open_text_editor(preferred="notes")
            else:
                speak_text("Opening the editor.")
                opened = open_text_editor()
            if opened:
                print("Editor opened.")
            else:
                print("Failed to open editor.")
            continue

        # Example response
        if "hello" in user_command:
            speak_text("Hello, Codefather. How can I help you today?")
        elif "who created you" in user_command:
            speak_text("You created me, Codefather. I'm Sage, your personal assistant.")
        elif "what time is it" in user_command:
            current_time = time.strftime("%I:%M %p")
            speak_text(f"It's {current_time} right now.")
        elif "what are you" in user_command:
            speak_text("I'm Sage, your interactive artificial intelligence assistant.")
        elif "schedule" in user_command:
            schedule()
        elif 'volume up' in user_command or 'increase volume' in user_command:
            speak_text("Turning the volume up.")
            try:
                # On macOS, use AppleScript to increase volume
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
            except Exception as e:
                print(f"Failed to increase volume: {e}")
        elif 'volume down' in user_command or 'decrease volume' in user_command:
            speak_text("Turning the volume down.")
            try:
                # On macOS, use AppleScript to decrease volume
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
            except Exception as e:
                print(f"Failed to decrease volume: {e}")
        elif 'mute' in user_command or 'mute volume' in user_command or 'volume mute' in user_command:
            speak_text("Muting the volume.")
            try:
                # On macOS, use AppleScript to mute volume
                subprocess.run(['osascript', '-e', 'set volume output muted true'])
            except Exception as e:
                print(f"Failed to mute volume: {e}")
        elif 'unmute' in user_command or 'unmute volume' in user_command or 'volume unmute' in user_command:
            speak_text("Unmuting the volume.")
            try:
                # On macOS, use AppleScript to unmute volume
                subprocess.run(['osascript', '-e', 'set volume output muted false'])
            except Exception as e:
                print(f"Failed to unmute volume: {e}")

        else:
            speak_text("I heard you, but I'm not sure what to do with that command yet.")


# import datetime
# import time

# import pyttsx3
# import speech_recognition as sr

# def initalize_speech_engine():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     rate =engine.getProperty('rate')
#     engine.setProperty('rate', rate-50)
#     volume = engine.getProperty('volume')
#     engine.setProperty('volume', volume+0.25)
#     return engine

# def speak_text(text):
#     engine = initalize_speech_engine()
#     engine.say(text)
#     engine.runAndWait()

# def command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source, duration=0.5)
#         print("Listening...", end="", flush=True)
#         # sensible defaults that satisfy Recognizer's assertions
#         r.pause_threshold = 0.8
#         r.non_speaking_duration = 0.5
#         r.dynamic_energy_threshold = True
#         r.dynamic_energy_adjustment_damping = 0.15
#         r.energy_threshold = 300
#         # keep the listen call limited so it doesn't block indefinitely
#         try:
#             audio = r.listen(source, phrase_time_limit=10)
#         except Exception as e:
#             print(f"Listening error: {e}")
#             return None

#         try:
#             print("\r", end="", flush=True)
#             print("Recognizing...", end="", flush=True)
#             text = r.recognize_google(audio, language='en-us')
#             print(f"You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("Sorry, I did not understand that.")
#             return None
#         except sr.RequestError:
#             print("Sorry, my speech service is down.")
#             return None

# def cal_day():
#     day = datetime.datetime.today().weekday() + 1
#     day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
#     if day in day_dict.keys():
#         day_of_week = day_dict[day]
#         print(f"Today is: {day_of_week}")
#     return day_of_week

# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     t = time.strftime("%I:%M %p")
#     day = cal_day()

#     if hour >= 0 and hour < 12 and 'AM' in t:
#         speak_text(f"Good Morning Codefather, It's {day} and the time is {t}.")
#     elif hour >= 12 and hour < 16 and 'PM' in t:
#         speak_text(f"Good Afternoon Codefather, It's {day} and the time is {t}.")
#     else:
#         speak_text(f"Good Evening Codefather, It's {day} and the time is {t}.")



# if __name__ == "__main__":
#     wishMe()
#     while True:
#         command = input("Enter your command (or type 'exit' to quit): ")


# # if __name__ == "__main__":
# #     while True:
# #         result = command()
# #         if not result:
# #             continue
# #         user_command = result.lower()
# #         if user_command:
# #             print(f"User Command: {user_command}")


# # speak_text("Hello, I am Sage")