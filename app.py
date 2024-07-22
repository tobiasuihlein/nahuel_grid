import streamlit as st
import streamlit.components.v1 as components
from functions import *
from PIL import Image
import base64
import io
import requests
import os

st.set_page_config(layout="wide")

html_code = f"""
<head>
    <title>ORGANIC GRIDS</title>
    <style>@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap')</style>
</head>
<body>
    <div style="text-align: center">
        <h1 style="font-family: Raleway;">ORGANIC GRIDS</h1>
    </div>
"""
components.html(html_code, height=60)

def fetch_image_from_url(url):
    # Download the image
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    
    # Convert the image to a BytesIO object
    image_bytes = io.BytesIO(response.content)
    
    # Optionally open it with PIL to ensure it's a valid image
    img = Image.open(image_bytes)
    
    # Reset the BytesIO pointer to the beginning
    image_bytes.seek(0)
    
    return image_bytes, img.format

# Create widgets to specify grid properties by user input
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2: rows = st.number_input(label="Number of rows", min_value=1, max_value=10, value=4, step=1)
    with col2: transition_size = st.slider(label="Transition size", min_value=0.1, max_value=5.0, value=2.5, step=0.1)

    with col3: cols = st.number_input(label="Number of columns", min_value=1, max_value=10, value=6, step=1)
    with col3: transition_speed = st.slider(label="Transition speed", min_value=0.1, max_value=5.0, value=2.5, step=0.1)
    transition_speed = 1 / transition_speed

# Create widget for image upload
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Set grid properties if no user input
if rows is None:
    rows = 4
    cols = 6
    transition_size = 2.5
    transition_speed = 1 / 2.5

# Disply image in grid
with st.container():

    if uploaded_image is None:
        url = "https://images.unsplash.com/photo-1573147367786-a5a227916f0c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        img_bytes, img_type = fetch_image_from_url(url)
        bytes_data = img_bytes.read()
        
    else:
        bytes_data = uploaded_image.read()
        img_type = uploaded_image.name.split('.')[1]

    # Convert bytes to image
    img = Image.open(io.BytesIO(bytes_data))
    img_width, img_height = img.size

    html_output = split_image_and_create_html_output(img, img_type, rows, cols, transition_speed, transition_size)

    components.html("", height=30)
    components.html(html_output, height=600)