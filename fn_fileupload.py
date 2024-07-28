import base64
import io
from PIL import Image
import streamlit as st


def process_image(default_image_data, question_key):
    new_upload = st.file_uploader(
        f"{question_key}", type=["png", "jpg", "jpeg"], label_visibility="hidden")

    if new_upload is None:
        if default_image_data is not None:
            try:
                # Decode the base64 string to bytes if it's not already bytes
                if isinstance(default_image_data, str):
                    default_image_data = base64.b64decode(default_image_data)
                default_image = Image.open(io.BytesIO(default_image_data))
                st.image(
                    default_image, caption="previous upload", width=100)
                buffered = io.BytesIO()
                default_image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(
                    buffered.getvalue()).decode("utf-8")
                new_upload_data = buffered.getvalue()
            except Exception as e:
                st.error(f"Failed to load default image: {e}")
                default_image, new_upload_data, image_base64 = None, None, None
        else:
            new_upload_data, image_base64 = None, None
    else:
        try:
            # open the uploaded object as image
            uploaded_image = Image.open(new_upload)
            # Specify new width and height
            new_width = 100
            # Calculate new height to maintain aspect ratio
            aspect_ratio = uploaded_image.height / uploaded_image.width
            new_height = int(new_width * aspect_ratio)

            # Resize the image
            resized_image = uploaded_image.resize((new_width, new_height))
            # display it to streamlit app or html
            st.image(uploaded_image, caption='', width=100)
            buffered = io.BytesIO()  # create a memory version of the image
            # eventhough the uploaded image was in other format, now it saves it as .PNG
            uploaded_image.save(buffered, format="PNG")
            new_upload_data = buffered.getvalue()
            image_base64 = base64.b64encode(
                buffered.getvalue()).decode("utf-8")
        except Exception as e:
            st.error(f"Failed to process uploaded image: {e}")
            uploaded_image, new_upload_data, image_base64 = None, None, None

    # return new_upload_data, image_base64
    # first used for database and second is for directly putting to .html template and pdf conversion
    return new_upload_data, image_base64
