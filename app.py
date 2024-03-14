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