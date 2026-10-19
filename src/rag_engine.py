import io
import os
import tempfile  # <-- Asegúrate de que esta línea está aquí
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from src.config import EMBEDDING_MODEL

class RAGEngine:   
    def __init__(self):
        """Inicializa con un vector store vacío."""
        self.embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = InMemoryVectorStore(self.embeddings)

    def process_document(self, uploaded_file):
        """
        Procesa un archivo subido por el usuario lo particiona y lo indexa.
        """
        # Cargar el texto según el tipo de archivo
        if uploaded_file.name.endswith(".pdf"):
            # Crear un archivo temporal en disco
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                # Escribir los bytes del archivo subido en el archivo temporal
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Pasar la RUTA del archivo temporal al cargador
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
            finally:
                # Eliminar el archivo temporal después de cargarlo
                os.unlink(tmp_file_path)
                
        elif uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
            docs = [Document(page_content=text, metadata={"source": uploaded_file.name})]
        else:
            raise ValueError("Formato no soportado. Sube un archivo .pdf o .txt")

        # Particionar el documento (Chunking)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
            add_start_index=True,
        )
        splits = text_splitter.split_documents(docs)

        # Añadir un ID y nombre de fuente a cada trozo para las citas
        for i, doc in enumerate(splits):
            doc.metadata["chunk_id"] = i
            doc.metadata["source"] = uploaded_file.name

        # Indexar en el vector store
        self.vector_store.add_documents(splits)
        return len(splits)

    def retrieve(self, query: str, k: int = 3) -> str:
        """
        Recupera los fragmentos más relevantes y los formatea.
        
        Args:
            query (str): La pregunta del usuario.
            k (int): Número de fragmentos a recuperar.
            
        Returns:
            str: Contexto formateado con citas de fuentes.
        """
        # Verificamos si el vector store está vacío, si no hay resultados, devolvemos un texto vacío.
        docs = self.vector_store.similarity_search(query, k=k)
        
        if not docs:
            return ""

        bloques = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "Desconocida")
            page = doc.metadata.get("page", "?")
            bloques.append(f"[Fuente {i}: {source}, pág {page}]\n{doc.page_content}")
            
        return "\n\n".join(bloques)