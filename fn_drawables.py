import json
import os
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import base64


def process_canvas(df, dq_number, use_previous=False):
    # Assuming df is your DataFrame and it's already defined
    # use instead: df['dq_number'].iloc[0]  # use the latter instead of  "" if you want previous drawing; but that is creating problem in that it is giving non editable drawing
    st.write(" ")
    st.write(" ")
    st.write(f"{dq_number}: Graphing question")

    if use_previous == True:
        dq_number = df['dq_number'].iloc[0]
    else:
        dq_number = ''

    # If dq_number is not None and not an empty string, load it as JSON
    if pd.notnull(dq_number) and dq_number != '':
        intdrawing = json.loads(dq_number)
        st.session_state['intdrawing'] = intdrawing
    else:
        # Existing code
        if 'intdrawing' not in st.session_state or st.session_state.intdrawing is None:
            if os.path.exists("intdrawing.json"):
                with open("intdrawing.json", "r") as f:
                    intdrawing = json.load(f)
            else:
                intdrawing = {}  # Initialize an empty state if the file doesn't exist
                with open("intdrawing.json", "w") as f:
                    json.dump(intdrawing, f)  # save the file as json file
            st.session_state['intdrawing'] = intdrawing

    intdrawing_json_form = json.dumps(
        st.session_state.intdrawing)  # is in json format
    intdrawing_json_form2 = json.loads(
        intdrawing_json_form)  # is in dictionary format

    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("line",  "point",  # "rect", "circle", "polygon", "freedraw",
                          "transform")
    )

    # stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3) # uncomment this if you want to give choice to the user to select the stroke width

    # if drawing_mode == 'point':
    #     point_display_radius = st.sidebar.slider(
    #         "Point display radius: ", 1, 25, 3)
    # stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    # bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # drawing_mode = "transform" if st.checkbox("Move ROIS", False) else "line" # This is Andrie's invention

    canvas_result_dq_number = st_canvas(
        background_color="white",
        fill_color="rgba(0, 151, 255, 0.3)",
        stroke_width=2,
        stroke_color="rgba(0, 50, 255, 0.7)",
        initial_drawing=intdrawing_json_form2,
        height=600,
        width=600,
        drawing_mode=drawing_mode,
        display_toolbar=True,
        update_streamlit=True,
        key=f"{dq_number}"
    )

    img_str_dq_number = None
    if canvas_result_dq_number.json_data is not None:
        objects = pd.json_normalize(
            canvas_result_dq_number.json_data["objects"])
        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        img_dq_number = Image.fromarray(canvas_result_dq_number.image_data)
        img_dq_numberb = img_dq_number.convert("RGB")  # Convert to RGB mode
        # Convert the PIL image to a base64 string
        buffered = BytesIO()
        img_dq_numberb.save(buffered, format="JPEG")
        # this is for the html template
        img_str_dq_number = base64.b64encode(buffered.getvalue()).decode()

    return canvas_result_dq_number.json_data, img_str_dq_number
