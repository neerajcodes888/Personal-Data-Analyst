import streamlit as st
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
import base64
from PIL import Image
from io import BytesIO

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

def save_image(base64_str, save_path):
    img = base64_to_image(base64_str)
    img.save(save_path)
    print(f"Image saved at {save_path}")

lida = Manager(text_gen = llm("openai")) 
textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)

menu = st.sidebar.selectbox("Choose an option" , ["Full Analysis","Custom Analysis"])

if menu == 'Full Analysis':
    