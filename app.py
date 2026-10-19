"""Punto de entrada de la aplicación Streamlit."""
import sys
import os
import streamlit as st
from src.rag_engine import RAGEngine
from src.agent import TouristAgent

# Añadir el directorio raíz al PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Configuración de la página ---
st.set_page_config(page_title="Asistente Turístico", page_icon="🌍", layout="wide")
st.title("🌍 Asistente Turístico Inteligente")

# --- Inicializar el Agente (siempre está listo) ---
@st.cache_resource
def get_agent():
    return TouristAgent()

agent = get_agent()

# --- Barra lateral para subir documentos ---
with st.sidebar:
    st.header("📄 Base de Conocimiento")
    st.write("Sube una guía turística en formato **PDF** o **TXT** para que el asistente pueda responder basándose en ella.")
    
    uploaded_file = st.file_uploader("Sube tu guía turística aquí", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        # Solo procesamos si el archivo es nuevo (evitamos reprocesar en cada recarga)
        if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
            with st.spinner("Procesando documento y creando índice vectorial..."):
                try:
                    rag = RAGEngine()
                    num_chunks = rag.process_document(uploaded_file)
                    st.session_state.rag = rag
                    st.session_state.current_file = uploaded_file.name
                    st.success(f"¡Documento procesado! ({num_chunks} fragmentos indexados).")
                except Exception as e:
                    st.error(f"Error al procesar el archivo: {e}")
        else:
            st.info(f"Documento activo: **{uploaded_file.name}**")
            
    if "rag" not in st.session_state:
        st.warning("⚠️ Sube un documento para empezar a hacer preguntas sobre él.")

# Gestión del estado del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interacción del usuario
if prompt_user := st.chat_input("Haz una pregunta (ej. '¿Cuánto cuesta la entrada?' o '¿Qué tiempo hará mañana?')"):
    
    # Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt_user})
    with st.chat_message("user"):
        st.markdown(prompt_user)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando y buscando en la guía..."): # <-- Spinner restaurado
            try:
                # Recuperar contexto si hay un documento cargado
                context = ""
                if "rag" in st.session_state:
                    context = st.session_state.rag.retrieve(prompt_user)
                
                # Comprobar si es pregunta de clima (respuesta instantánea)
                if "tiempo" in prompt_user.lower() or "clima" in prompt_user.lower():
                    response_text = agent.generate_response(
                        question=prompt_user, context=context, chat_history_list=st.session_state.messages
                    )
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Si es RAG, usamos Streaming
                else:
                    response_text = st.write_stream(
                        agent.stream_response(
                            question=prompt_user, 
                            context=context, 
                            chat_history_list=st.session_state.messages
                        )
                    )
                    
                    # Guardamos la respuesta completa en el historial
                    if response_text:
                        if isinstance(response_text, list):
                            response_text = "".join(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
            except Exception as e:
                st.error(f"Lo siento, ha ocurrido un error: {e}")