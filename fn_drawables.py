
import pandas as pd  # pip install pandas
import numpy as np  # pip install numpy
from PIL import Image  # pip install pillow
import streamlit as st  # pip install streamlit
# pip install streamlit-drawable-canvas # to install from pypi
from streamlit_drawable_canvas import st_canvas
import io
from io import BytesIO
import base64
import seaborn as sns  # pip install seaborn
import matplotlib.pyplot as plt  # pip install matplotlib


def process_canvas(default_drawing_data):
    canvas_width = 600
    canvas_height = 500

    # xx = st.number_input("Pick a number up to 1000", 0, 1000, key="xx")
    # yy = st.number_input("Pick a number up to 1000", 0, 1000, key="yy")

    # if xx is not 0:
    #     x_lim = [0, xx]
    # else:
    #     x_lim = [0, 100]
    # if yy is not 0:
    #     y_lim = [0, yy]
    # else:
    #     y_lim = [0, 100]

    x_lim = [0, 100]
    y_lim = [0, 100]

    xsteps = (x_lim[1]-x_lim[0])/10
    ysteps = (y_lim[1]-y_lim[0])/10

    # constant that are mentioned in
    scaleFactors = [x_lim[1], y_lim[1], .1214, .775]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set the limits of the plot
    ax.set_xlim([x_lim[0], x_lim[1]])
    ax.set_ylim([y_lim[0], y_lim[1]])

    # Set the labels of the plot
    ax.set_xlabel('Quantity, Q')
    ax.set_ylabel('Price, P')

    # Specify the locations of the grid lines
    # Grid lines from 0 to 10 with a step of z
    x_ticks = np.arange(x_lim[0], x_lim[1] + 1, xsteps)
    # Grid lines from 0 to 10 with a step of z
    y_ticks = np.arange(y_lim[0], y_lim[1] + 1, ysteps)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # Draw a grid
    ax.grid(True)

    # Use streamlit to display the plot
    # st.pyplot(fig)

    # Convert the matplotlib figure to a PIL Image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    bg_image = Image.open(buf)

    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", (   # "freedraw",
            "line",
            "curve",
            "coordinate",
            # "singlearrowhead",
            # "doublearrowhead",
            "text",
            "rect",  # "point",  # "circle",
            "polygon",
            "transform"
        )
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider(
            "Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    # bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    # bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    # Add a text input field for the label when the drawing mode is "text"
    # label = st.sidebar.text_input("Label: ") if drawing_mode == "text" else None

    # Create a canvas component
    canvas_result = st_canvas(
        # Fixed fill color with some opacity
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        # background_color=bg_color,
        # background_image=Image.open(bg_image) if bg_image else None,
        background_image=bg_image,
        update_streamlit=realtime_update,
        width=canvas_width,
        height=canvas_height,
        drawing_mode=drawing_mode,
        # text=label,  # Use the entered label as the text to be drawn
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        scaleFactors=scaleFactors,  # [80, 40],
        key="canvas",
    )

    # st.write("Canvas data:", canvas_result)

    # Do something interesting with the image data and paths
    # if canvas_result.image_data is not None:
    if canvas_result.image_data is not None:
        # Display the image data
        # to automatically display the image in the streamlit app (kind of duplicate canvas)
        # st.image(canvas_result.image_data)
        # Convert the image data to a PIL Image
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

        # Resize the user-drawn image to match the size of the background image
        img = img.resize(bg_image.size)
        # Combine the user-drawn image and the background image
        combined = Image.alpha_composite(bg_image.convert('RGBA'), img)

        # Save the combined image to a BytesIO object
        combined_io = io.BytesIO()
        combined.save(combined_io, 'PNG')
        combined_io.seek(0)

        # Convert the combined image to a base64 encoded string to be saved to database or template
        base64_combined = base64.b64encode(combined_io.getvalue()).decode()
        upload2db = base64_combined
        # # Save img to a BytesIO object for comparison
        # img_io = io.BytesIO()
        # img.save(img_io, 'PNG')
        # img_io.seek(0)

        # # Convert img to a base64 encoded string
        # base64_img = base64.b64encode(img_io.getvalue()).decode()

        # # Compare the base64 encoded strings
        # if base64_combined == base64_img:
        #     # img and combined are the same, which means nothing was drawn
        #     upload2db = default_drawing_data
        # else:
        #     upload2db = base64_combined

        # # Create a download button for the image
        # st.download_button(
        #     label="Download-canvas-image",
        #     # data=img_io,
        #     data=combined_io,
        #     file_name='image01.png',
        #     mime='image/png'
        # )
        return upload2db

    # # Do something interesting with the JSON data
    # if canvas_result.json_data is not None:
    #     # need to convert obj to str because PyArrow
    #     objects = pd.json_normalize(canvas_result.json_data["objects"])
    #     for col in objects.select_dtypes(include=['object']).columns:
    #         objects[col] = objects[col].astype("str")
    #     st.dataframe(objects)
