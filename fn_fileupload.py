import base64
import io
from PIL import Image
import streamlit as st


def process_image(df, qno):
    # Get the blob data of the first row for the file upload
    default_image_data = df[qno].iloc[0]

    # Create a file uploader
    st.write(" ")
    st.write(" ")

    new_upload = st.file_uploader(
        f"{qno}: Upload Image or Graph, Please no .HIEC format", type=["png", "jpg", "jpeg"])

    # If no file is uploaded, use the default image
    if new_upload is None:
        if default_image_data is not None:
            try:
                # Convert the blob data to a bytes object and open it as an image
                default_image = Image.open(io.BytesIO(default_image_data))
                new_upload_dict = default_image_data
                st.image(default_image, caption='',  width=50)
                # Convert image to base64 string
                buffered = io.BytesIO()
                default_image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(
                    buffered.getvalue()).decode("utf-8")
            except Exception:
                # If the image data cannot be opened, set the variables to None
                default_image = None
                new_upload_dict = None
                image_base64 = None
        else:
            new_upload_dict = ''  # None
            image_base64 = ''  # None
    else:
        new_upload = Image.open(new_upload)
        st.image(new_upload, caption='', width=50)
        # Convert image to base64 string
        buffered = io.BytesIO()
        new_upload.save(buffered, format="PNG")
        new_upload_dict = buffered.getvalue()
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return new_upload_dict, image_base64
