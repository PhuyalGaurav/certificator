import os
import shutil
import zipfile
import base64
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(layout="wide")
def sanitize_name(name):
    return ''.join(e for e in name if e.isalnum())

def generate_certificate(template_path, names, coordinates, font):
    path = "certificates"
    os.makedirs(path, exist_ok=True)

    for name in names:
        sanitized_name = sanitize_name(name)
        template = Image.open(template_path)
        draw = ImageDraw.Draw(template)
        x, y = coordinates

        draw.text((x, y), name, fill="black", font=font)

        certificate_path = f"{path}/{sanitized_name}.png"
        template.save(certificate_path)
        st.text(f"Generated certificate for {name}.")

    zip_file_name = "certificates.zip"
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for root, _, files in os.walk("certificates"):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.basename(file_path))

    shutil.rmtree("certificates")  # Remove the "certificates" folder

    # Create a download button for the zip file
    with open(zip_file_name, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download=\'{zip_file_name}\'>\
            Click to download {zip_file_name}\
        </a>'
        st.markdown(href, unsafe_allow_html=True)
        st.text("The download link will expire in 10 seconds.")
    
    time.sleep(10)  # Wait for 60 seconds
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)  # Remove the zip file after 60 seconds

def get_click_coords(image_file):
    st.text("Click on the Image From where you want to start writing the text :")
    if image_file is not None:
        image = Image.open(image_file)
        image_array = np.array(image)
        coords = streamlit_image_coordinates(image_array)
        if coords is not None:
            return (coords['x'], coords['y'])
            st.text(f"Coordinates selected: {coords['x']}, {coords['y']}")
        else:
            st.warning('No coordinates selected on the image.')
            return None
    

def main():
    st.title("Certificate Generator")

    st.header("Instructions")
    st.markdown("""
    1. Upload an image file.
    2. Click on the image to select the coordinates where you want to write the text.
    3. Enter the font size.
    4. Enter the names (one per line).
    5. Click the 'Generate Certificates' button.
    """)
    image_file = st.file_uploader('Upload image file', type=['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'gif', 'svg', 'ico'])
    coordinates = get_click_coords(image_file)

    font_file = st.file_uploader('Use Default Font: America.ttf, or :', type=['ttf'])
    font_size = st.number_input('Enter font size', min_value=1, value=24)
    names = st.text_area('Enter names (one per line)')

    if image_file and names and coordinates:
        image_file.seek(0)  # Reset the file pointer to the beginning of the file
        font_file = font_file or open('america.ttf', 'rb')  # Use uploaded font file or default font file
        font = ImageFont.truetype(font_file, font_size)
        generate_certificate(image_file, names.split('\n'), coordinates, font)

if __name__ == "__main__":
    main()