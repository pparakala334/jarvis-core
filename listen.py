import speech_recognition as sr

def capture_input():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2.0  # wait for 1 second of silence before stopping
    mic = sr.Microphone()

    print("🎙️ Listening... (speak now or type)")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
        return recognizer.recognize_google(audio)

    except sr.WaitTimeoutError:
        return input("⌨️ You (typed): ")
    except sr.UnknownValueError:
        return input("❌ Couldn't understand — type it instead: ")
    except Exception as e:
        print(f"Mic error: {e}")
        return input("⌨️ You (typed): ")
