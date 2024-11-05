from PIL import Image
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

'''

def show_title_image():
    cols = st.columns([1, 1, 1])
    with cols[1]:
        logo_big_path = "assets/img/logo_CyG.png"
        image = Image.open(logo_big_path)
        resized_image = image.resize((int(image.width * 200 / image.height), 200))  # Adjust the height to 20 pixels
        st.image(resized_image)
'''

def show_icon_image():
    cols = st.columns([1, 2, 1])
    with cols[0]:
        st.image(Image.open("assets/img/logo_codexca_tiny.png", ), width=40)
    with cols[1]:
        st.markdown("<h1 style='display: inline-block; vertical-align: middle;'>Asistente Virtual</h1>",
                    unsafe_allow_html=True)


def show_footer():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap');
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            text-align: right;
            padding: 10px;
            font-size: 14px;
            color: grey;
            font-family: 'Manrope', sans-serif;
        }
        </style>
        <div class="footer">
            Made with &#10084 by Mottum.</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input("OpenAI API Key",
                                                                                                    type="password",
                                                                                                    key='openai_api_key_input')
