import pyttsx3

engine = pyttsx3.init()
def get_available_voices(engine):
    return engine.getProperty('voices')

def select_voice_by_gender(engine, gender):
    available_voices = get_available_voices(engine)
    
    for voice in available_voices:
        if gender.lower() in voice.name.lower():
            return voice.id
    
    return None

def text_to_speech(text, speaking_mode='default'):
    engine = pyttsx3.init()

    # Set speaking mode
    if speaking_mode == 'female':
        voice_id = select_voice_by_gender(engine, 'female')
    elif speaking_mode == 'male':
        voice_id = select_voice_by_gender(engine, 'male')
    elif speaking_mode == 'robot':
        # Implement your own robot voice settings
        engine.setProperty('rate', 120)  # Adjust the speech rate for a robotic effect
        engine.setProperty('volume', 0.9)  # Adjust the volume for a robotic effect
        engine.setProperty('pitch', 50)  # Adjust the pitch for a robotic effect
        voice_id = None
    else:
        voice_id = None  # Use the default voice

    if voice_id:
        engine.setProperty('voice', voice_id)

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text_input = input("What do you want to Convert to Speech: ")
    speaking_mode_input = input("Enter speaking mode (female, male, robot): ")

    text_to_speech(text_input, speaking_mode_input)
