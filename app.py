
# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
import logging
logging.getLogger('easyocr').setLevel(logging.ERROR)

# Import libraries
import streamlit as st
import easyocr
import os
import shutil
from PIL import Image

# Set destination folder
folder = 'car_plates'
os.makedirs(folder, exist_ok=True)

# Page title and description
st.title("License Plate Recognition App")
st.write("Upload a car image to detect the plate number")

# File uploader widget
uploaded = st.file_uploader("Choose an image", type=['jpg','png','jpeg'])

# Only runs if a file was uploaded
if uploaded:

    # Display uploaded image
    image = Image.open(uploaded)
    st.image(image, caption=uploaded.name)

    # Save temporarily to disk for EasyOCR
    temp_path = uploaded.name
    with open(temp_path, 'wb') as f:
        f.write(uploaded.getbuffer())

    # Copy file to car_plates folder
    dst = os.path.join(folder, uploaded.name)
    shutil.copy2(temp_path, dst)
    # st.info("Saved " + uploaded.name + " to car_plates folder")

    # Load EasyOCR and read plate
    reader = easyocr.Reader(['en'])
    results = reader.readtext(temp_path)

    # Remove temp file
    os.remove(temp_path)

    # Filter results above 65% confidence
    detected = []
    for (bbox, text, conf) in results:
        if conf > 0.65:
            detected.append((text, conf))

    # Display results or show unable to detect
    if detected:
        for text, conf in detected:
            st.success("Detected Plate Number: " + text + " (" + str(round(conf * 100)) + "% Confidence)")
    else:
        st.error("Unable to detect number plate")

# Add footer
st.markdown("---")
st.caption("Built by Mithirendra M")
