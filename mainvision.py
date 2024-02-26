# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:45:01 2024

@author: gsahani
"""

from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai

# Directly define your Google API key here
GOOGLE_API_KEY = ''

genai.configure(api_key=GOOGLE_API_KEY)

##Function to load gemini pro vision

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

##initialize our streamlit app

html_temp = """
    <div style="background-color:#010200;padding:10px">
    <h2 style="color:white;text-align:center;">Invoice Data Extractor</h2>
    </div>
    """    
st.markdown(html_temp,unsafe_allow_html=True)

image = Image.open('Image.png') 

st.image(image, use_column_width=True)

html_temp1 = """
    <div style="background-color:#010200">
    <p style="color:white;text-align:center;" >Designed & Developed By: <b>Gaurav R. Sahani</b> </p>
    </div>
    """
st.markdown(html_temp1,unsafe_allow_html=True)

st.subheader("Invoice data extraction using Gemini AI")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Upload Invoice Image...", use_column_width=True)

input=st.text_input("Please enter Input Prompt: ",key="input")

submit=st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("Output response is..")
    st.write(response)

