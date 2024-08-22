import speech_recognition as sr
import requests
import pyttsx3
import json
import time

def listen_and_convert():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
    try:
        text = r.recognize_sphinx(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("PocketSphinx could not understand audio")
        return None
    except sr.RequestError as e:
        print("PocketSphinx error; {0}".format(e))
        return None

def query_phi3(text):
    prompt = "Short answer only: " + text
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                                     json={'model': 'phi', 'prompt': prompt})
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                print("Failed to connect to Ollama after multiple attempts")
                return "I'm sorry, I couldn't process your request at this time."

def speak_response(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        user_input = listen_and_convert()
        if user_input:
            response = query_phi3(user_input)
            print("Phi-3 response:", response)
            speak_response(response)

if __name__ == "__main__":
    main()
