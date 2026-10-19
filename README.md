# Asistente Turístico Inteligente (RAG + LLM)

Este proyecto es una aplicación web desarrollada con **Streamlit** para el front y usando un API Key **Google Gemini**. Su objetivo es actuar como un asistente turístico capaz de leer guías en formato PDF o TXT, responder preguntas basándose en ese documento y una simulacion de consulta del clima.

## Características principales

- **RAG Dinámico (Retrieval-Augmented Generation):** El usuario puede subir cualquier guía turística en PDF o TXT. El sistema procesa el texto, lo divide en fragmentos, genera embeddings y los indexa en un almacén vectorial en memoria.
- **Diálogo Multiturno:** Mantiene el contexto de la conversación (memoria de los últimos turnos) para responder a preguntas de seguimiento.
- **Function Calling (Herramientas):** Integración de una herramienta externa `get_weather` que devuelve la predicción del tiempo, con manejo de errores y registro de logs (auditoría).
- **Streaming de respuestas:** Las respuestas del modelo se muestran en tiempo real (palabra a palabra) para mejorar la experiencia de usuario.

## Tecnologías utilizadas

- **Python 3.12**
- **uv:** Gestor de entornos y dependencias ultrarrápido.
- **Streamlit:** Interfaz frontal de usuario web.
- **LangChain:** Orquestación agéntica del LLM, prompts, historial y RAG.
- **Google Gemini:** Modelo de lenguaje (LLM) y modelo de embeddings.
- **PyPDF:** Extracción de texto de documentos PDF.

## Estructura del proyecto

```text
asistente-turistico/
├── app.py
├── pyproject.toml
├── .env
├── README.md
└── src/
    ├── __init__.py
    ├── config.py     
    ├── rag_engine.py
    ├── agent.py        
    └── tools.py
```    