# Informe final: Asistente turístico inteligente

## Diseño de la solución
La solución se ha diseñado bajo una arquitectura modular orientada a objetos, separando claramente las responsabilidades:
- **Capa de Presentación (`app.py`):** Interfaz de usuario en Streamlit.
- **Capa de Recuperación (`rag_engine.py`):** Encargada de leer, trocear y vectorizar la documentación (PDF/TXT) introducida por el usuario.
- **Capa de Razonamiento (`agent.py`):** Configuración del LLM, gestión de historial multiturno (memoria) y generación de respuestas en streaming.
- **Capa de Herramientas (`tools.py`):** Funciones externas (Function Calling) aisladas del resto de la lógica.

Esta separación permite que, por ejemplo, el motor de RAG pueda ser reutilizado en un backend con FastAPI sin necesidad de modificar una sola línea de código.

## Decisiones técnicas
- **Uso de `uv`:** Se ha seleccionado `uv` frente a `pip` o `poetry` por su velocidad de resolución e instalación de dependencias, y su integración nativa con el archivo `pyproject.toml`.
- **Google Gemini (versión Flash):** Se ha utilizado la familia `gemini-flash-latest` por su excelente equilibrio entre velocidad, ventana de contexto y coste. Para los embeddings, se utiliza el modelo actual `models/gemini-embedding-001`, que sustituye al obsoleto `embedding-001`.
- **InMemoryVectorStore:** Al tratarse de un prototipo que procesa documentos en caliente (subidos por el usuario), se ha utilizado un almacén vectorial en memoria. Para producción, se migraría a FAISS persistente o ChromaDB.
- **Historial multiturno controlado:** Para evitar sobrepasar el límite de tokens de la API de Google, el historial se trunca a los últimos 4 mensajes antes de enviarlo al LLM. Además, se transforma del formato de Streamlit al formato de mensajes nativo de LangChain (`HumanMessage` y `AIMessage`).
- **Streaming:** Implementado mediante generadores de Python (`yield`) y la función `st.write_stream` de Streamlit, mejorando notablemente la experiencia de usuario al no tener que esperar a que el modelo termine de generar toda la respuesta.
- **Function Calling con Logs:** Se ha implementado una función `get_weather` simulada. Para cumplir el requisito de auditoría, se utiliza la librería estándar `logging` de Python, registrando cada llamada, la fecha y el error.

## Resultados
El prototipo cumple con todos los requisitos funcionales:
1. **RAG:** El sistema recupera información semántica del PDF y es capaz de citar la página y el documento exacto.
2. **Multiturno:** Responde a preguntas de seguimiento (*"¿Cuánto cuesta el museo?" -> "¿Hay descuentos?"*) sin perder el hilo.
3. **Function Call:** Responde a preguntas meteorológicas de forma instantánea sin necesidad de consultar el PDF, limpiando y manejando errores si la fecha no es válida.

## Limitaciones y mejora futura
- **Persistencia:** Al usar un vector store en memoria, si el usuario recarga la página de Streamlit, deberá volver a subir el documento. La mejora pasa por implemntar una base de datos para persitir la información.
- **Tool del clima simulada:** Actualmente, la llamada de la herramienta del tiempo se hace mediante una comprobación de palabras clave (tiempo y clima). 
- **Evaluación automática:** No se han implementado métricas matemáticas de evaluación (como RAGAS). *Mejora:* Crear un dataset de preguntas y respuestas y evaluar la precisión del contexto y la fidelidad de la respuesta (groundedness).
- **Multimodalidad:** En el futuro se podría extender el soporte para que el usuario suba fotos de la zona or egion y el LLM (mediante visión) pueda dar informacinón de las mismas.