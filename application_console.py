import speech_recognition as sr
import pyttsx3

def robot_voice_settings(engine):
    # Adjust voice settings for a robot-like sound
    engine.setProperty('rate', 150)  # Adjust the speech rate
    engine.setProperty('volume', 1.0)  # Adjust the volume

def speak_with_robot_voice(engine, text):
    robot_voice_settings(engine)
    engine.say(text)
    engine.runAndWait()

def select_voice_by_gender(engine, gender):
    available_voices = engine.getProperty('voices')
    
    for voice in available_voices:
        if gender.lower() in voice.name.lower():
            return voice.id
    
    return None

def text_to_speech(engine, text, speaking_mode='default'):
    # Set speaking mode
    if speaking_mode == 'female':
        voice_id = select_voice_by_gender(engine, 'female')
    elif speaking_mode == 'male':
        voice_id = select_voice_by_gender(engine, 'male')
    elif speaking_mode == 'robot':
        speak_with_robot_voice(engine, text)
        return
    else:
        voice_id = None  # Use the default voice

    if voice_id:
        engine.setProperty('voice', voice_id)

    engine.say(text)
    engine.runAndWait()

def speech_to_text(rec):
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
                return rec.recognize_google(audio2)

        except sr.RequestError as e:
            print("Could not request output; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown Error")

if __name__ == "__main__":
    rec = sr.Recognizer()
    engine = pyttsx3.init()

    while True:
        print("Select operation:")
        print("1. Speech to Text")
        print("2. Text to Speech")
        print("3. Exit")

        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            text_input = speech_to_text(rec)
            print("Speech to Text Result:", text_input)
        elif choice == '2':
            text_input = input("What do you want to Convert to Speech: ")
            speaking_mode_input = input("Enter speaking mode (female, male, robot): ")
            text_to_speech(engine, text_input, speaking_mode_input)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
