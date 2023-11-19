import streamlit as st
import speech_recognition as sr
import pyttsx3

# In-memory storage for user data
users = {"user1": {"password": "password1", "preferences": {"voice": "default"}}}
# In-memory storage for conversion history
conversion_history = {"user1": []}

class SessionState:
    def __init__(self, **kwargs):
        self.username = None
        self.logged_in = False

def robot_voice_settings(engine):
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
            st.info("Please wait. Calibrating microphone...")
            rec.adjust_for_ambient_noise(source2, duration=5)
            st.success("Microphone calibrated")

            # Getting user input 
            audio2 = rec.listen(source2, timeout=3) 

            # Use Google to recognize the input
            return rec.recognize_google(audio2)

    except sr.RequestError as e:
        st.error(f"Could not request output; {e}")
        return None

    except sr.UnknownValueError:
        st.warning("Unknown Error")
        return None

def authenticate_user(username, password):
    if username in users and users[username]["password"] == password:
        return True
    return False

def save_conversion_history(username, operation, input_text, result):
    history_entry = {"operation": operation, "input_text": input_text, "result": result}
    conversion_history[username].append(history_entry)

def get_conversion_history(username):
    return conversion_history.get(username, [])

def main():
    st.title("Speech Processing Application")

    session_state = SessionState()

    # Get user input for authentication
    if not session_state.logged_in:
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        if st.button("Log In"):
            if authenticate_user(username, password):
                session_state.logged_in = True
                session_state.username = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password.")
                return

    
    rec = sr.Recognizer()

    operation = st.sidebar.radio("Select Operation", ("Speech to Text", "Text to Speech", "History"))

    print(f"Selected operation: {operation}")

    if operation == "Speech to Text":
        st.subheader("Speech to Text")
        text_result = speech_to_text(rec)
        print("Reached after speech_to_text")
        if text_result:
            st.success(f"Speech to Text Result: {text_result}")
            save_conversion_history(session_state.username, "Speech to Text", "", text_result)
        else:
            st.error("Failed to recognize speech.")
    elif operation == "Text to Speech":
        print("Reached Text to Speech")
        st.subheader("Text to Speech")
        text_input = st.text_input("Enter text for Text to Speech:")
        speaking_mode_input = st.selectbox("Select speaking mode", ("default", "female", "male", "robot"))

        if st.button("Convert to Speech"):
            text_to_speech(text_input, speaking_mode_input)
            st.success("Text converted to speech.")
            save_conversion_history(session_state.username, "Text to Speech", text_input, "")
    elif operation == "History":
        print("Reached History")
        st.subheader("Conversion History")
        history = get_conversion_history(session_state.username)
        if history:
            st.table(history)
        else:
            st.info("No conversion history.")

if __name__ == "__main__":
    main()
