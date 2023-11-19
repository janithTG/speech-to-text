import streamlit as st
import speech_recognition as sr
import pyttsx3
import time

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
    try:
        # Setting microphone as input device
        with sr.Microphone() as source2:
            st.info("Calibrating microphone. Please wait...")

            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02) 
                progress_bar.progress(i + 1)

            rec.adjust_for_ambient_noise(source2, duration=1)  # Adjust for ambient noise for a shorter duration
            st.success("Microphone calibrated. You can speak now.")

            # Getting user input 
            audio2 = rec.listen(source2, timeout=3)  # Capture audio for a maximum of 3 seconds

            
            with st.spinner("Processing..."):
                # Use Google to recognize the input
                text_result = rec.recognize_google(audio2)

            st.empty()  
            #st.success(f"Speech to Text Result: {text_result}")
            return text_result

    except sr.RequestError as e:
        st.empty()
        st.error(f"Could not request output; {e}")
        return None

    except sr.UnknownValueError:
        st.empty()
        st.warning("Speech not recognized. Please try again.")
        return None

def main():
    st.title("Speech Processing Application")

    rec = sr.Recognizer()
    engine = pyttsx3.init()

    operation = st.sidebar.radio("Select Operation", ("Speech to Text", "Text to Speech"))

    if operation == "Speech to Text":
        st.subheader("Speech to Text")
        if st.button("Start Speaking"):
            text_result = speech_to_text(rec)
            if text_result:
                st.success(f"Speech to Text Result: {text_result}")
            else:
                st.error("Failed to recognize speech.")

    elif operation == "Text to Speech":
        st.subheader("Text to Speech")
        text_input = st.text_input("Enter text for Text to Speech:")
        speaking_mode_input = st.selectbox("Select speaking mode", ("default", "female", "male", "robot"))
        
        if st.button("Convert to Speech"):
            text_to_speech(engine, text_input, speaking_mode_input)
            st.success("Text converted to speech.")

if __name__ == "__main__":
    main()
