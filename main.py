import os

from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from src.utils import *
from src.pages.pag1_home import show_home_page
# TODO: Cambiar este import pag2_chats para probar la ultima version experimental
from src.pages.pag2_chats_prev import show_chats_page
from src.pages.pag3_help import show_help_page
from src.pages.pag4_demostrador_2 import show_demostrador_page
from PIL import Image

icon = Image.open("assets/img/logo_CyG.png")

st.set_page_config(page_title="Agente de transporte", page_icon=icon, initial_sidebar_state="collapsed",
                   layout="wide")

load_dotenv()

cols = st.columns([1, 3, 1])
with cols[1]:
    col1, col2 = st.columns([2, 1])
    with col2:
        st.image("assets/img/logo_CyG.png", width=120)
    with col1:
        st.markdown("<h1 style='display: inline-block; vertical-align: middle;'>Agente de transporte</h1>",
                    unsafe_allow_html=True)



# openai_api_key = os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input("OpenAI API Key", type="password")


if "pagina_seleccionada" not in st.session_state:
    st.session_state.pagina_seleccionada = "Ayuda"

# Por defecto la pagina de Inicio
if "menu" not in st.session_state:
    st.session_state.menu = "Ayuda"


# Function to handle page selection change
def on_change(key):
    st.session_state.pagina_seleccionada = st.session_state.menu


def main():
    # Create the option menu and bind it to session state
    option_menu(
        menu_title=None,
        options=["Ayuda", "Demostrador"],
        icons=["house-fill", "chat-left-dots-fill"],
        orientation="horizontal",
        key="menu",
        default_index=["Ayuda", "Demostrador"].index(st.session_state.pagina_seleccionada),
        on_change=on_change
    )

    # Display the selected page
    '''
    if st.session_state.pagina_seleccionada == "Inicio":
        show_home_page()
    elif st.session_state.pagina_seleccionada == "Conversaciones":
        show_chats_page()
    '''
    if st.session_state.pagina_seleccionada == "Ayuda":
        show_help_page()

    elif st.session_state.pagina_seleccionada == "Demostrador":
        show_demostrador_page()

    show_footer()


if __name__ == '__main__':
    main()
