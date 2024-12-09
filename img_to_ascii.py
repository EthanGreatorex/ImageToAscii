import streamlit as st
import PIL.Image
from PIL import Image as PilImage, ImageDraw, ImageFont
import io

# ASCII characters used for conversion
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    """Converts the image to grayscale."""
    progress_bar.progress(60, text="Almost done!")
    return image.convert("L")

def pixel_to_ascii(pixel_value):
    """Converts a pixel value to an ASCII character based on brightness."""
    return ASCII_CHARS[pixel_value // 25] 

def image_to_ascii(image, new_width):
    """Converts an image to ASCII art."""
    progress_bar.progress(40, text=progress_text)
    # Resize and convert the image to grayscale
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    
    ascii_str = ""
    
    # Process each pixel in the image
    for y in range(image.height):
        for x in range(image.width):
            pixel_value = image.getpixel((x, y))
            ascii_str += pixel_to_ascii(pixel_value)
        ascii_str += "\n"  # Add new line after each row
    
    # final string
    return ascii_str

def ascii_to_image(ascii_str, new_width):
    """Converts ASCII art back to an image."""
    progress_bar.progress(80, text="So close!")
    # black background image
    image = PilImage.new('RGB', (new_width * 10, len(ascii_str.split('\n')) * 12), color=(0,0,0))
    draw = ImageDraw.Draw(image)
    
    font = ImageFont.load_default() 
    
    # Draw each ASCII character as a pixel
    y_offset = 0
    for line in ascii_str.split('\n'):
        x_offset = 0
        for char in line:
            draw.text((x_offset, y_offset), char, font=font, fill=(255, 255, 255))
            x_offset += 10  # Move 10 pixels for each character
        y_offset += 12  # Move 12 pixels down after each line

    return image

# Streamlit page configuration
st.set_page_config(layout="wide")

# Title and instructions
st.title(f"Image to Ascii Image Converter 😊")
st.subheader("Choose an image to start!\n _please no more than 200mb or I get too tired_ 🥱")

# File uploader widget
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

st.subheader("Size of the image result")
image_size = st.select_slider("",[100,150,200,250,300,350,400])

if uploaded_file:
    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0, text=progress_text)

    progress_bar.progress(20, text=progress_text)

    WIDTH = image_size

    # Open image file
    image = PilImage.open(uploaded_file)

    # Convert image to ASCII art
    ascii_str = image_to_ascii(image, new_width=WIDTH)
    
    # Convert ASCII art back to image
    ascii_image = ascii_to_image(ascii_str, new_width=WIDTH)

    progress_bar.progress(100, text="Finished!")

    # Display the ASCII art image
    st.image(ascii_image, caption="Generated ASCII Art Image")
    
    # Button to download the ASCII art image
    buffered = io.BytesIO()
    ascii_image.save(buffered, format="PNG")
    buffered.seek(0)
    
    # Note -> mime is telling the browser that we are giving it an image not text
    st.download_button(
        label="Download ASCII Art Image",
        data=buffered,
        file_name="ascii_art_image.png",
        mime="image/png"
    )
else:
    st.write("Waiting for file upload 💤💤")
