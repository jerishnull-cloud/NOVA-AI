import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os


# =========================
# NOVA Voice Engine
# =========================

engine = pyttsx3.init()

recognizer = sr.Recognizer()


def speak(text):
    print("NOVA:", text)

    engine.say(text)
    engine.runAndWait()


def listen():

    print("\n🎙️ NOVA is listening...")

    sample_rate = 16000
    duration = 6

    try:

        print("🎤 Speak now...")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        filename = temp_file.name
        temp_file.close()

        write(
            filename,
            sample_rate,
            recording
        )

        with sr.AudioFile(filename) as source:

            audio = recognizer.record(source)

        print("🧠 NOVA is processing...")

        command = recognizer.recognize_google(audio)

        print("YOU:", command)

        os.remove(filename)

        return command

    except sr.UnknownValueError:

        print("NOVA: I couldn't understand you.")

        return ""

    except sr.RequestError:

        print("NOVA: Speech recognition service is unavailable.")

        return ""

    except Exception as e:

        print("NOVA microphone error:", e)

        return ""