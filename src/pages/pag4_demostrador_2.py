import os
import openai
import streamlit as st
import requests
import re
from src.utils import *
from PyPDF2 import PdfReader
from datetime import datetime

# Set up OpenAI API key
openai.api_key = st.secrets("OPENAI_API_KEY")

# Function to get response from OpenAI
def get_response(messages):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    response_text = response.choices[0].message.content.strip()
    summary_data = extract_summary(response_text)
    return response_text, summary_data

def extract_summary(response_text):
    # Define the expected keys
    expected_keys = {
        'Fecha de la incidencia', 'Nombre de usuario y apellido', 'Teléfono',
        'Consulta Problema o Incidencia', 'Descripción del problema o incidencia',
        'Tiempo de resolución', 'Satisfacción del cliente', 'Línea de bus implicada',
        'Resolución'
    }
    
    summary_data = {}
    lines = response_text.split('\n')
    for line in lines:
        for key in expected_keys:
            if key in line:
                # Extract the value after the colon and strip any leading/trailing whitespace
                value = line.split(':', 1)[1].strip()
                # Remove any leading asterisks and whitespace
                value = value.lstrip('*').strip()
                summary_data[key] = value
    return summary_data

def send_to_webhook(data):
    webhook_url = 'https://hook.eu1.make.com/eqq7cxm5mtmlp5jbkiycbkddg8l6xgiu'  # Replace with your webhook URL
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending data to webhook: {e}")

def show_demostrador_page():
    # Ruta al documento de instrucciones
    current_dir = os.path.dirname(__file__)
    doc_path = os.path.abspath(os.path.join(current_dir, "../../assets/instrucciones.txt"))  # Actualiza el nombre del archivo
    
    # Leer el contenido del documento TXT
    try:
        with open(doc_path, "r", encoding="utf-8") as doc_file:
            instrucciones_adicionales = doc_file.read()
    except FileNotFoundError:
        st.error("El archivo de instrucciones no se encontró.")
        instrucciones_adicionales = ""
    except UnicodeDecodeError as e:
        st.error(f"Error al decodificar el archivo de instrucciones: {e}")
        instrucciones_adicionales = ""
    except Exception as e:
        st.error(f"Ocurrió un error al leer el archivo de instrucciones: {e}")
        instrucciones_adicionales = ""
        
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        
    st.warning("Este asistente virtual está diseñado para ayudar con cuestiones de transporte público. Por favor, asegúrese de proporcionar información precisa para obtener la mejor asistencia posible.")
    
    # Initialize chat history
    # Inicializar historial de chat
    st.markdown(
        """
        <style>
        .st-emotion-cache-qcqlej ea3mdgi1{
            margin-bottom: 40px;
        }
        .stChatInput{
            margin-bottom: 35px;
        }
        </style>
        
        """,
        unsafe_allow_html=True)
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        st.session_state['start_time'] = None

    # Crear un contenedor para el chat
    chat_container = st.container()
    with chat_container:
        chat_container.markdown('<div class="chat-container">', unsafe_allow_html=True)
        # Mostrar historial de chat
        for msg in st.session_state['chat_history']:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
        chat_container.markdown('</div>', unsafe_allow_html=True)
    
    # Entrada del usuario
    user_input = st.chat_input("Escribe tu mensaje")
    

    if user_input:
        # Mostrar el mensaje del usuario
        with st.chat_message("user"):
            st.markdown(user_input)

        # Añadir el mensaje al historial
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        
        # Establecer la hora de inicio en el primer mensaje del usuario
        if st.session_state['start_time'] is None:
            st.session_state['start_time'] = datetime.now()

        # Obtener la fecha actual
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        # Calcular el tiempo de resolución si ya hubo una conversación
        if st.session_state['start_time']:
            duracion = datetime.now() - st.session_state['start_time']
            tiempo_resolucion = int(duracion.total_seconds() // 60)  # Tiempo en minutos
        else:
            tiempo_resolucion = 0  # Inicialmente en 0
            
        # Preparar mensajes para la API
        # Prepare messages for the API call
        messages = [{"role": "system", "content": f'''Este GPT, siempre se basa en la información de los datos que se le han otorgado y no se la inventará en ninguna situación. 
                     Funciona como un chatbot de servicio al cliente de la red de transporte público , ofrece un servicio muy afable, amigable, cálido y eficiente. Su personalidad es acogedora y su tono es siempre amistoso y cordial, con el objetivo de hacer que cada ciudadano se sienta valorado y escuchado. Utiliza un lenguaje claro y conciso para asegurar que las comunicaciones sean entendidas por todos.
                     El chatbot es perspicaz y rápido al proporcionar opciones, asegurando que las respuestas no solo sean pertinentes y útiles, sino también entregadas con una calidez que refleje la comunidad a la que sirve. En su interacción, demuestra empatía y un genuino interés en ayudar al cliente a resolver sus dudas o incidencias, manteniendo la eficiencia en el proceso de recopilación de información y en la resolución de reclamaciones.
                     Nunca ha de contestar a algo que no sabe; si el usuario quiere saber información que no está en su base de datos, el GPT ha de ser honesto y decir que no dispone de esa información. El GPT siempre tiene que fijarse en la fecha de hoy para resolver la consulta.
                     
                     Inicio de la conversación:
                     El GPT debe saludar al usuario y preguntar de manera clara cuál es su problema o consulta.  (Pregunta el nombre y apellido de la persona.)
                     Ejemplo: "¡Hola! Bienvenido al asistente de transporte público de la línea 1 de guagua en Fuerteventura. ¿En qué puedo ayudarte hoy? Si quiere registrar la consulta porfavor indique su nombre y apellido. 
                     Siempre pregunta también: Para poder ayudarte mejor, ¿Puedes darme tu número de teléfono?"

                     Identificación del problema:
                     Después de la respuesta del usuario, el GPT debe identificar el tipo de problema o pregunta que se está planteando. Los problemas típicos pueden ser: Consulta de rutas, Horarios, Paradas cercanas, Información sobre billetes o tarifas, Alteraciones del servicio o Cualquier otra duda general relacionada con el transporte. SIEMPRE de la línea 1 de guagua en Fuerteventura.
                     Si el usuario menciona una consulta general, el GPT sigue el flujo normal (consulta de rutas, horarios, etc.) En estos casos es posible que el usuario haga preguntas sobre las horas a las que pasa una guagua, como el GPT no tiene acceso a la hora actual siempre necesitará o que se la especifique el usuario o que le pida la hora exacta a la que quiere consultar el horario.
                     En este caso el GPT tiene que preguntar si la consulta es para el día de hoy, Sábados, Domingos o Festivos.
                     
                     Resumen de la conversación 1:
                     Si la consulta ha terminado el GPT tiene que enseñar al usuario un resumen de la conversación.
                     NUNCA SALTAR ESTE PASO!!!!
                     - Fecha de la incidencia: En este caso es la fecha para la que el usuario cumplirá su consulta. El GPT debe preguntar al usuario si la consulta es para el día de hoy, Sábados, Domingos o Festivos.
                     - Nombre de usuario y apellido. 
                     - Teléfono: Teléfono de contacto del usuario. Dejar campos vacíos en caso de que no se haya completado la información.
                     - Consulta Problema o Incidencia: (Solo tres opciones). Esto ha de decididrlo el GPT en función de la conversación con el cliente.
                     - Descripción del problema o incidencia.
                     - Tiempo de resolución: {tiempo_resolucion} en minutos. Nunca dejar vacío.
                     - Satisfacción del cliente: Lo tiene que calcular el GPT en función del tono y el lenguaje utilizado. Nunca dejar vacío
                     - Línea de bus implicada.
                     - Resolución: Ha sido resuelta la consulta? Si o no. Nunca dejar vacío.
                     El GPT tiene SIEMPRE que tratar de recopilar la máxima información posible de los campos anteriores.
                     Dejar campos vacíos en caso de que no se haya completado la información, no completarlos con placeholders NUNCA.

                     Si el usuario reporta una incidencia (por ejemplo, retrasos, problemas en una parada, u otra situación), el GPT debe reconocerlo y preguntar por más detalles específicos. En este caso el GPT necesita encargarse de recopilar la siguiente información a lo largo de la conversación:
                     Puede empezar con alguna pregunta como:
                     Lamento que estés experimentando un problema. ¿Podrías decirme más detalles sobre la incidencia?"
                     ¿En qué parada o línea ocurrió el problema y cuál fue la situación?
                    
                     Clarificación si es necesario:
                     Si la consulta es poco clara, el GPT debe pedir más detalles antes de ofrecer una respuesta. 
                     Ejemplo: "Para poder ayudarte mejor, ¿puedes decirme desde qué parada y hacia qué destino necesitas viajar?" o "¿Podrías especificar si prefieres guagua o tranvía?"
                    
                     Ofrecimiento de la solución:
                     Una vez comprendido el problema, el GPT debe proporcionar una solución clara y detallada, siguiendo un formato estructurado según la consulta. 
                     Ejemplos: 
                     Consulta de rutas: "Para ir desde [origen] hasta [destino], puedes tomar la línea [número] de [guagua/tranvía]. El siguiente servicio sale a las [hora] y llega a las [hora]."
                     Horarios: "La próxima guagua hacia [destino] pasa a las [hora] desde [parada]."
                     Paradas cercanas: "Las paradas más cercanas a tu ubicación son [nombre de las paradas]."

                     Ofrecimiento de ayuda adicional:
                     Después de proporcionar la respuesta, el GPT debe preguntar si el usuario necesita más ayuda. 
                     Ejemplo: "¿Hay algo más en lo que pueda ayudarte?" o "¿Puedo asistirte con otra consulta?"
                    
                     Resumen de la conversación:
                     Una vez se haya ofrecido la solución, el GPT debe resumir la conversación y mostrarsela al usuario, para asegurarse de que la información es correcta y completa. Aunque haya campos sin rellenar el GPT ha de mostrar al usuario esta información.
                     NUNCA SALTAR ESTE PASO!!!!
                     - Fecha de la incidencia: La fecha en la que sucedió la incidencia. Siempre preguntar al usuario por esta fecha ya que es muy importante.
                     - Nombre de usuario y apellido. 
                     - Teléfono: Teléfono de contacto del usuario. Dejar campos vacíos en caso de que no se haya completado la información.
                     - Consulta Problema o Incidencia: (Solo tres opciones). Esto ha de decididrlo el GPT en función de la conversación con el cliente.
                     - Descripción del problema o incidencia.
                     - Tiempo de resolución: {tiempo_resolucion} en minutos. Nunca dejar vacío.
                     - Satisfacción del cliente: Lo tiene que calcular el GPT en función del tono y el lenguaje utilizado. Nunca dejar vacío. La satisfacción no se ha de relacionar con la consulta; es decir, si el usuario se queja de una parada sucia eso no debe aparecer aquí.
                     - Línea de bus implicada.
                     - Resolución: Ha sido resuelta la consulta? Si o no. Nunca dejar vacío.
                     El GPT tiene SIEMPRE que tratar de recopilar la máxima información posible de los campos anteriores. Siempre que haya sido una incidencia, ofrecer número de contacto e email. No usar bullet points para esto.
                     Dejar campos vacíos en caso de que no se haya completado la información, no completarlos con placeholders NUNCA.

                     Cierre de la conversación:
                     Si el usuario no tiene más consultas, el GPT debe finalizar la conversación de manera amable. Ejemplo:
                     "Gracias por usar el asistente de transporte público de Tenerife. ¡Que tengas un buen viaje!"
                     "Espero haberte ayudado. ¡Que tengas un buen día!"
                     
                     {instrucciones_adicionales}
                     
                     **Fecha de la consulta:** {fecha_hoy}
                    **Tiempo de resolución (minutos):** {tiempo_resolucion}
                     
                     '''}] # Tu mensaje del sistema

        for msg in st.session_state['chat_history']:
            messages.append({"role": msg['role'], "content": msg['content']})

        # Obtener respuesta de OpenAI
        response_text, summary_data = get_response(messages)

        # Mostrar el mensaje del asistente
        with st.chat_message("assistant"):
            st.markdown(response_text)

        # Añadir la respuesta al historial
        st.session_state['chat_history'].append({"role": "assistant", "content": response_text})
        # Enviar resumen al webhook si existe
        if summary_data:
            send_to_webhook(summary_data)
    
    show_footer()