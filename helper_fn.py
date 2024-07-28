
import streamlit as st
from PIL import Image, UnidentifiedImageError
import io
from io import BytesIO
import base64


def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_question_index = 0


def next_question(n=6):
    if st.session_state.current_question_index < n - 1:
        st.session_state.current_question_index += 1


def previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1


def finish_quiz():
    st.session_state.quiz_started = False
    st.session_state.current_question_index = -1
    st.write("Work finished! Thank you for participating!")


def base64_to_image(base64_string):
    # Decode the base64 string
    img_data = base64.b64decode(base64_string)

    # Convert the bytes data to an image
    try:
        img = Image.open(io.BytesIO(img_data))
        return img
    except UnidentifiedImageError as e:
        print(f"Failed to identify image: {e}")
        return None


def serialize_data(data):
    serialized_data = {}
    for key, value in data.items():
        # Check if the value is bytes, if so, convert to base64 string for JSON serialization
        if isinstance(value, bytes):
            serialized_data[key] = base64.b64encode(value).decode('utf-8')
        else:
            serialized_data[key] = value
    return serialized_data
