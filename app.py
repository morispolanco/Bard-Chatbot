import streamlit as st
from streamlit_chat import message
from bardapi import Bard
import json

# Cargar la configuración desde un archivo JSON
with open('config.json') as config_file:
    data = json.load(config_file)

# Obtener la clave de la API de Bard desde la configuración
bard_api_key = data.get("BARD_API_KEY")

# Inicializar la API de Bard
bard = Bard(token=bard_api_key, timeout=30)

# Función para generar la respuesta del chatbot
def generate_response(prompt):
    history = "\n".join(f"User: {u}\nBard Response: {b}" for u, b in zip(st.session_state.user_responses, st.session_state.bard_responses))
    response = bard.get_answer(f"Conversation History: {history}\n{prompt}")
    return response.get("content", "Error en la respuesta de Bard")

# Función para manejar el clic en el botón "New Topic"
def on_btn_click():
    st.session_state.user_responses.clear()
    st.session_state.bard_responses.clear()

# Función para manejar el cambio en el campo de entrada de texto
def on_input_change():
    user_input = st.session_state.user_input
    output = generate_response(user_input)
    st.session_state.user_responses.append(user_input)
    st.session_state.bard_responses.append(output)
    st.session_state.user_input = ""

# Configuración de la interfaz de usuario
st.title("Bard Chatbot")
st.button("New Topic", on_click=on_btn_click)

# Inicialización del estado de la sesión
if 'user_responses' not in st.session_state:
    st.session_state.user_responses = []

if 'bard_responses' not in st.session_state:
    st.session_state.bard_responses = []

# Entrada de texto para la respuesta del usuario
user_input = st.text_input("User Response:", on_change=on_input_change, key="user_input")

# Mostrar un spinner mientras se obtiene la respuesta de Bard
with st.spinner("Loading..."):
    # Mostrar el historial del chat en orden inverso
    for i, (user_resp, bard_resp) in enumerate(reversed(list(zip(st.session_state.user_responses, st.session_state.bard_responses)))):
        message(f"**User {i + 1}:** {user_resp}", is_user=True)
        message(f"**Bard Response {i + 1}:** {bard_resp}")
