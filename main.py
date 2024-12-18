import os

from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from src.utils import *
from src.pages.pag1_home import show_home_page
# TODO: Cambiar este import pag2_chats para probar la ultima version experimental
from src.pages.pag3_help import show_help_page
from src.pages.pag4_demostrador_2 import show_demostrador_page
from PIL import Image

st.set_page_config(
    page_title="Agente de transporte",  
    initial_sidebar_state="expanded", 
    layout="wide",
    menu_items={
        'About': """
            ### Sobre Nosotros
            
            **Control y Gestión S.A.** es una empresa líder en soluciones de transporte público, dedicada a mejorar la experiencia de viaje de nuestros ciudadanos mediante tecnologías innovadoras y servicios de alta calidad.
            
            - **Dirección:** Calle Falsa 123, Ciudad, País
            - **Correo Electrónico:** contacto@controlygestion.com
            - **Teléfono:** +34 912 345 678
            
            ### Derechos de Autor
            
            © 2023 Control y Gestión S.A. Todos los derechos reservados.
            
            ### Síguenos
            
            [Facebook](https://www.facebook.com/tuempresa) | [Twitter](https://www.twitter.com/tuempresa) | [LinkedIn](https://www.linkedin.com/company/tuempresa)
        """,
        'Get Help': "mailto:soporte@controlygestion.com",  # Enlace mailto
        'Report a bug': "https://github.com/tuempresa"  # URL válida para reportar bugs
    }
)

load_dotenv()

with st.sidebar:
    st.image("assets/img/logo_CyG.png", use_column_width=True)
    
    #st.markdown("### Sistema de participación ciudadana para el transporte.")
    #st.markdown("Este agente de transporte permite obtener información sobre el transporte público de la ciudad, registrar reclamaciones, hacer sugerencias y recibir asistencia en tiempo real.")
    
    st.markdown("### Cuadro de mandos de incidencias")
    st.markdown("Visita nuestro dashboard para ver las incidencias reportadas por los ciudadanos.")
    st.markdown(
        """
        <style>
        /* Estilos para el botón personalizado */
        .custom-button {
            background-color: #D3362A; /* Rojo */
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 5px;
            transition: box-shadow 0.3s ease;
        }

        /* Efecto de sombra al pasar el cursor */
        .custom-button:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }

        /* Contenedor para centrar el botón */
        .button-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        </style>
        
        <div class="button-container">
            <a href="https://airtable.com/appuQhUEXX0XCagcv/shrrJ8aHWdOapChtS" target="_blank">
                <button class="custom-button">
                    Visitar Dashboard
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
    
    # Disclaimers
    st.markdown("### Advertencias")
    st.warning("Nuestros modelos pueden sufrir alucinaciones. 🤖")


if "pagina_seleccionada" not in st.session_state:
    st.session_state.pagina_seleccionada = "Agente Ciudadano"

# Por defecto la pagina de Inicio
if "menu" not in st.session_state:
    st.session_state.menu = "Agente Ciudadano"


# Function to handle page selection change
def on_change(key):
    st.session_state.pagina_seleccionada = st.session_state.menu


def main():
    st.markdown(
    """
    <style>
    .main-title {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stSidebar"]{
        max-width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="main-title">
            <h1>Sistema de participación ciudadana</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="text-align: center; font-size: smaller;">
            Este agente de transporte permite obtener información sobre el transporte público de la ciudad, registrar reclamaciones, hacer sugerencias y recibir asistencia en tiempo real.
        </div>
        """,
        unsafe_allow_html=True
    )
    # Create the option menu and bind it to session state
    option_menu(
        menu_title=None,
        options=["Agente Ciudadano", "Ayuda"],
        icons=["house-fill", "chat-left-dots-fill"],
        orientation="horizontal",
        key="menu",
        default_index=["Agente Ciudadano", "Ayuda"].index(st.session_state.pagina_seleccionada),
        on_change=on_change
    )

    # Display the selected page
    
    #if st.session_state.pagina_seleccionada == "Inicio":
        #show_home_page()
    #elif st.session_state.pagina_seleccionada == "Conversaciones":
        #@show_chats_page()

    if st.session_state.pagina_seleccionada == "Ayuda":
        show_help_page()
        

    if st.session_state.pagina_seleccionada == "Agente Ciudadano":
        show_demostrador_page()

    show_footer()
if __name__ == '__main__':
    main()
