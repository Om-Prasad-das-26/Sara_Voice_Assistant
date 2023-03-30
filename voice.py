import speech_recognition as sr
import webbrowser
import keyboard
import pyttsx3
import datetime
import geocoder
import requests
import pywhatkit


# Initialize the speech recognition engine
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
engine.setProperty('voice', voice_id)

# Use the speak() function to speak
engine.say("Hello, I am sara the voice assistant, how may i help you??")
engine.runAndWait()

# Define a function to capture user speech input or prompt for manual input
def get_input():
    with sr.Microphone() as source:
        print("SPEAK NOW...")
        audio = r.listen(source)
        try:
            # Use the speech recognition engine to convert audio to text
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print("Could not request results from the speech recognition service; {0}".format(e))

    # If speech recognition fails, prompt user to enter command manually
    return input("Please enter a command: ")

# Define functions to perform various tasks
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    if hour > 12:
        hour -= 12
    speak("The time is {0}:{1} {2}".format(hour, minute, "AM" if now.hour < 12 else "PM"))

def turn_off_lights():
    # Code to turn off the lights goes here
    speak("The lights have been turned off.")


# Define a function to play a song from YouTube
def talk(command):
    engine.say("playing "+command)
    
def takecommand():
    listener= sr.Recognizer()
    speak("What song would you like me to play?")
    try:
        with sr.Microphone() as source:
            print("Listening......")
            voice= listener.listen(source)
            command= listener.recognize_google(voice)
            song = command.replace('play','')
            
            talk(song)
            pywhatkit.playonyt(song)
    
    except:
        pass


# Define a function to fetch the current weather data 
def get_current_weather(city_name):
    
    API_KEY = "400da1dace0250c0d5744c4200083d8e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The current weather in {city_name} is {description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("Sorry, I was unable to fetch the current weather data.")

# Define a function to get the user's current city based on their IP address using the geocoder module
def get_current_city():
    g = geocoder.ip('me')
    city_name = g.city
    return city_name

def get_current_location():
    url = "https://ipinfo.io/json"
    response = requests.get(url)
    data = response.json()
    city = data["city"]
    region = data["region"]
    country = data["country"]
    speak(f"You are currently in {city}, {region}, {country}")


# Define a function to generate speech output
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a dictionary to map user commands to functions
command_map = {
    "hello": greet,
    "what time is it": tell_time,
    "goodbye": exit,
    "turn off the lights" : turn_off_lights,
    "play me a song" : takecommand,
    "what's the weather" : lambda: get_current_weather(get_current_city()),
    "my current location" : lambda: get_current_location(),
    
}

# Main program loop
while True:
    # Get user input
    input_text = get_input()

    # Process user input and generate response
    if input_text in command_map:
        command_map[input_text]()
    else:
        speak("Sorry, I didn't understand that command.") 