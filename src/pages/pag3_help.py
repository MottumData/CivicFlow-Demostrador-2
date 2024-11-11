import streamlit as st
from src.utils import *

def show_help_page():
    
    st.markdown("""
        Bienvenido a la página de ayuda del **Chatbot de Asistencia Ciudadana**. Aquí encontrarás información sobre cómo utilizar el chatbot para realizar consultas, reportar incidencias o compartir sugerencias. Tus aportaciones serán enviadas a nuestra base de datos en Airtable y procesadas por nuestro equipo.
    """)
    
    st.markdown(
        """
        <style>
        
        .centered img {
            margin: 20px 0;
        }
        .st-emotion-cache-1wmy9hl.e1f1d6gn1 {
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        ### ¿Qué puedes hacer con el chatbot?

        - **Consultas:** Realiza preguntas sobre servicios, horarios, trámites y más.
        - **Incidencias:** Reporta problemas o situaciones que requieren atención.
        - **Sugerencias:** Comparte tus ideas para mejorar los servicios públicos.

        ### ¿Cómo utilizar el chatbot?

        1. **Inicia una conversación** en la página principal.
        2. **Identifícate** con tu nombre y, opcionalmente, proporciona un número de contacto.
        3. **Describe tu consulta, incidencia o sugerencia** de manera detallada.
        4. **Recibe asistencia** y continúa la conversación si necesitas más ayuda.

        ### Procesamiento de tus mensajes

        - Tus mensajes se envían a **Airtable** para ser gestionados.
        - Nuestro equipo revisa cada aportación y toma las acciones necesarias.
        - Podrías ser contactado si proporcionaste información de contacto y es necesario.

        ### Consejos para un mejor servicio

        - Proporciona **detalles específicos** como fechas, lugares y descripciones claras.
        - Sé **claro y conciso** para facilitar el entendimiento de tu solicitud.
        - Revisa las **Preguntas Frecuentes** más abajo para ver si tu duda ya fue resuelta.

        ### Preguntas Frecuentes

        """)

        with st.expander("¿Cómo reporto una incidencia?"):
            st.write("Para reportar una incidencia, inicia una conversación con el chatbot y proporciona detalles sobre el problema que deseas reportar.")
        with st.expander("¿Puedo mantener el anonimato?"):
            st.write("Sí, puedes optar por no proporcionar tu nombre o información de contacto. Sin embargo, esto podría limitar nuestra capacidad para darte seguimiento.")
        with st.expander("¿Cuánto tiempo tardan en responder?"):
            st.write("Nuestro equipo trabaja para responder lo más pronto posible. Los tiempos de respuesta pueden variar según la complejidad de la solicitud.")

        st.markdown("""
        ### Contacto Directo

        Si necesitas asistencia adicional, puedes contactarnos a través de:

        - **Correo electrónico:** soporte@asistenciaciudadana.com
        - **Teléfono:** +34 900 123 456

        ¡Gracias por contribuir a mejorar nuestros servicios!

        """)

        #st.image("assets/chatbot_help.png", use_column_width=True)