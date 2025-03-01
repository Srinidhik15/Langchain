from dotenv import load_dotenv

load_dotenv()  #load all env variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# configuring API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#we have 2 models:
## gemini-pro: optimized for test-only prompts
## gemini-pro-vision: optimized for text and image prompts

# Create a function to load Gemini Pro Vision model and get response
def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash-002')   # loading the genai gemini model
    response = model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,  # get mime type of uploaded file
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# Initialize streamlit app

st.set_page_config(page_title="Gemini Image Invoice extractor")

st.header("Gemini application")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices.You will 
receive input images as invoices and you will have to 
answer based on the input image
"""

# If submit button is clicked---image convert to bytes and and get image info 
# later image info with prompt should hit the gemini pro

if submit:
    image_data=input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)

    st.subheader("the response is")  # here we get the response
    st.write(response)