from PIL import Image
import streamlit as st
import os
from dotenv import load_dotenv
import base64

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
    # Obtener la ruta absoluta de la imagen
    current_dir = os.path.dirname(__file__)
    image_path = os.path.abspath(os.path.join(current_dir, "../assets/img/Logo_footer.png"))
    
    # Codificar la imagen en Base64
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        encoded_string = "" 
        
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap');
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: dark;
            text-align: right;
            padding: 10px;
            font-size: 14px;
            color: grey;
            font-family: 'Manrope', sans-serif;
            z-index: 999;
        }}
        
        .footer img {{
            height: 80px; /* Ajusta el tamaño según tus necesidades */
            margin-right: 10px; /* Espacio entre la imagen y el texto */
        }}
        </style>
        <div class="footer">
            <img src="data:image/png;base64,{encoded_string}" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input("OpenAI API Key",
                                                                                                    type="password",
                                                                                                    key='openai_api_key_input')
