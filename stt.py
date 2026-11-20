import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening... speak now")
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("No speech heard")
            return ""
    try:
        text = r.recognize_google(audio, language="en-IN")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand")
        return ""
    except sr.RequestError:
        print("Check your internet connection")
        return ""

if __name__ == "__main__":
    print("You said:", listen())