import os

from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from src.utils import *
from src.pages.pag1_home import show_home_page
# TODO: Cambiar este import pag2_chats para probar la ultima version experimental
from src.pages.pag2_chats_prev import show_chats_page
from src.pages.pag3_help import show_help_page
from PIL import Image

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

icon = Image.open("assets/img/logo_codexca_tiny.png")

st.set_page_config(page_title="Asistente Virtual", page_icon=icon, initial_sidebar_state="collapsed",
                   layout="wide")

show_title_image()

st.markdown("<h1 style='text-align: center;'>Asistente Virtual</h1>", unsafe_allow_html=True)



# openai_api_key = os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input(
#     "OpenAI API Key", type="password")


if "pagina_seleccionada" not in st.session_state:
    st.session_state.pagina_seleccionada = "Inicio"

# Por defecto la pagina de Inicio
if "menu" not in st.session_state:
    st.session_state.menu = "Inicio"


# Function to handle page selection change
def on_change(key):
    st.session_state.pagina_seleccionada = st.session_state.menu


def main():
    # Create the option menu and bind it to session state
    option_menu(
        menu_title=None,
        options=["Inicio", "Conversaciones", "Ayuda"],
        icons=["house-fill", "chat-left-dots-fill", "person-raised-hand"],
        orientation="horizontal",
        key="menu",
        default_index=["Inicio", "Conversaciones", "Ayuda"].index(st.session_state.pagina_seleccionada),
        on_change=on_change
    )

    # Display the selected page
    if st.session_state.pagina_seleccionada == "Inicio":
        show_home_page()
    elif st.session_state.pagina_seleccionada == "Conversaciones":
        show_chats_page()
    elif st.session_state.pagina_seleccionada == "Ayuda":
        show_help_page()

    show_footer()


if __name__ == '__main__':
    main()
