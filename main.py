import datetime
import time
import webbrowser

import pyttsx3
import speech_recognition as sr
import platform
import subprocess
import shutil
import os


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
        speak_text(f"Good morning Codefather. It's {day}, and the time is {current_time}.")
    elif 12 <= hour < 16:
        speak_text(f"Good afternoon Codefather. It's {day}, and the time is {current_time}.")
    else:
        speak_text(f"Good evening Codefather. It's {day}, and the time is {current_time}.")


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
        speak_text("Opening Facebook.")
        webbrowser.open("https://www.facebook.com")
        # Add code to open Facebook
    elif "instagram" in command:
        speak_text("Opening Instagram.")
        webbrowser.open("https://www.instagram.com")
        # Add code to open Instagram
    elif "twitter" in command:
        speak_text("Opening Twitter.")
        webbrowser.open("https://www.twitter.com")
        # Add code to open Twitter
    elif "linkedin" in command:
        speak_text("Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")
    elif "github" in command:
        speak_text("Opening GitHub.")
        webbrowser.open("https://www.github.com")
        
    else:
        speak_text("Sorry Codefather, I cannot access that social media platform at the moment.")

if __name__ == "__main__":
    # Uncomment this line if you want to see all available voices on your computer
    # show_available_voices()

    wish_me()

    while True:
        result = listen_for_command()

        if not result:
            continue

        user_command = result.lower()

        if ('facebook' in user_command or 'instagram' in user_command or 'twitter' in user_command or 'linkedin' in user_command):
            social_media(user_command)

            # speak_text("Sorry Codefather, I cannot access social media platforms at the moment.")
            # continue

        if "exit" in user_command or "quit" in user_command or "stop" in user_command:
            speak_text("Goodbye Codefather.")
            break

        print(f"User Command: {user_command}")

        # handle quick built-in actions
        if any(kw in user_command for kw in ("open notepad", "open textedit", "open text edit", "open editor", "open code editor", "open notes", "open note")):
            if "note" in user_command or "notes" in user_command or "notepad" in user_command:
                speak_text("Opening Notes")
                opened = open_text_editor(preferred="notes")
            else:
                speak_text("Opening editor")
                opened = open_text_editor()
            if opened:
                print("Editor opened.")
            else:
                print("Failed to open editor.")
            continue
        # Example response
        if "hello" in user_command:
            speak_text("Hello Codefather. How can I help you?")
        if "who created you" in user_command:
            speak_text("Codefather is a software developer and the creator of Sage, your personal assistant.")
        if "what time is it" in user_command:
            current_time = time.strftime("%I:%M %p")
            speak_text(f"The current time is {current_time}.")
        if "what are you" in user_command:
            speak_text("I am Sage, an interactive artificial consciousness.")
        else:
            speak_text("I heard you, but I do not have a command for that yet.")


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