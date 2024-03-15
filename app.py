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

