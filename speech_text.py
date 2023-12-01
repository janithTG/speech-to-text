import speech_recognition as sr
import pyttsx3

rec = sr.Recognizer()
engine = pyttsx3.init()  

def robot_voice_settings():
    engine = pyttsx3.init()
    # Adjust voice settings for a robot-like sound
    engine.setProperty('rate', 150)  # Adjust the speech rate
    engine.setProperty('volume', 1.0)  # Adjust the volume
    return engine

def speak_with_robot_voice(text):
    engine = robot_voice_settings()
    engine.say(text)
    engine.runAndWait()

def recordInput():
    while True:
        try:
            # Setting microphone as input device
            with sr.Microphone() as source2:
                print("Please wait. Calibrating microphone...")
                rec.adjust_for_ambient_noise(source2, duration=5)
                print("Microphone calibrated")

                # Getting user input 
                audio2 = rec.listen(source2) 

                # Use Google to recognize the input
                mytext = rec.recognize_google(audio2)

                return mytext

        except sr.RequestError as e:
            print("Could not request output; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown Error")

def outputText(text, speaking_mode='default'):
    global engine  # Use the globally defined engine variable

    # Opening a text file
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()

    # Set speaking mode
    if speaking_mode == 'female':
        engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Index 1 for female voice
    elif speaking_mode == 'male':
        engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Index 0 for male voice
    elif speaking_mode == 'robot':
        speak_with_robot_voice(text)  # Use the robot voice settings
        return

    # Speak the text using default settings
    engine.say(text)
    engine.runAndWait()

while True:
    text = recordInput()
    outputText(text, speaking_mode='male')  # Change speaking_mode as needed

    print("Done")
