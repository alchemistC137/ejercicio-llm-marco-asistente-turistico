from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.config import GENERATION_MODEL
from src.tools import get_weather

class TouristAgent:
    
    def __init__(self):
        """Inicializa el modelo y el prompt del sistema."""
        self.llm = init_chat_model(GENERATION_MODEL, model_provider="google_genai")
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Eres un asistente turístico experto. Responde en español usando el contexto proporcionado en el archivo adjuntando. "
             "Si el contexto está vacío o no contiene la respuesta, explica respetuosamente que no tienes información sobre eso "
             "y sugiere al usuario que suba un documento (PDF o TXT) con la información turística. "
             "Si el usuario te pregunta por el clima, usa tu herramienta de clima. "
             "Cita las fuentes usadas al final de tu respuesta.\n\n"
             "Contexto recuperado:\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

    def stream_response(self, question: str, context: str, chat_history_list: list):
        """
        Genera la respuesta del LLM en modo streaming.
        """
        # Convertir el historial
        chat_history = []
        for msg in chat_history_list[-4:]:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            else:
                chat_history.append(AIMessage(content=msg["content"]))

        messages = self.prompt.invoke({
            "context": context,
            "chat_history": chat_history,
            "question": question
        })
        
        # Generador que va devolviendo trozos de texto
        for chunk in self.llm.stream(messages):
            # Filtramos la firma de Google y devolvemos solo el texto
            if hasattr(chunk, "content") and chunk.content:
                if isinstance(chunk.content, str):
                    yield chunk.content
                elif isinstance(chunk.content, list):
                    for block in chunk.content:
                        if isinstance(block, dict) and "text" in block:
                            yield block["text"]

    def generate_response(self, question: str, context: str, chat_history_list: list) -> str:
        """
        Genera una respuesta directa (sin streaming) para herramientas específicas como el clima.
        """
        # Interceptar preguntas sobre el clima (Function Calling simulado)
        if "tiempo" in question.lower() or "clima" in question.lower():
            fecha = "mañana" if "mañana" in question.lower() else "hoy"
            return f"🌤️ **Predicción del tiempo:** {get_weather(fecha)}"
        
        # Si por alguna razón llega aquí sin ser clima, devolvemos un mensaje por defecto
        return "No tengo información suficiente."