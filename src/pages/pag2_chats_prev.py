import os
import tempfile

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma

from conf.project_path import CHROMA_DB_PATH
from src.utils import show_footer


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


# TODO Cambiar los mensajes que se muestran al cargar el documento
class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Context Retrieval en progreso**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        # self.status.write(f"**Question:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata.get("source", "Desconocido"))
            self.status.write(f"**Document {idx} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")


@st.cache_resource(ttl="8h")
def configure_retriever(uploaded_files):
    docs = []
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
        loader = PyPDFLoader(temp_filepath)
        docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=2,
                                                   separators=["\n\n", "\n", ".", " ", ""])
    splits = text_splitter.split_documents(docs)

    embeddings_model_name = "sentence-transformers/all-MiniLM-L12-v2"

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    # Se crea la base de datos de vectores en memoria
    # vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
    #

    # Se crea el directorio para almacenar la base de datos de Chroma
    vectordb = Chroma.from_documents(splits, embeddings, collection_name='documentos_adjuntos',
                                     persist_directory=CHROMA_DB_PATH)
    # vectordb.persist()
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 5})

    return retriever


def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input("OpenAI API Key",
                                                                                                    type="password",
                                                                                                    key='openai_api_key_input')


def show_chats_page():
    st.write("Chats")
    st.sidebar.write("Conversaciones")
    openai_api_key = get_openai_api_key()
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    model_name = st.sidebar.selectbox("Selecciona un modelo", ["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
                                      index=3)
    st.write("Modelo seleccionado:", model_name)
    uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=True)

    retriever = configure_retriever(uploaded_files) if uploaded_files else None

    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

    llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True)

    if retriever:
        # Ajustamos la plantilla para incluir el contexto de documentos
        prompt_template = ChatPromptTemplate.from_template(
            "Eres un asistente IA experto en documentación y análisis. Presta mucha atención a las fechas que "
            "aparecen en diferentes formatos.\n"
            "Historial de conversación:\n{chat_history}\n"
            "Información relevante:\n{context}\n"  # Este es el contexto de los documentos recuperados
            "Pregunta: {question}\n"
            "Responde de la manera más concisa posible a la consulta basada en la información relevante:"
        )
        # TODO Cambiar la función ConversationalRetrievalChain por create_retrieval_chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            verbose=False,
            combine_docs_chain_kwargs={
                "prompt": prompt_template,
                "document_variable_name": "context"  # Aseguramos que la variable se llame 'context'
            }
        )
    else:
        # Prompt en caso de que no haya retriever
        prompt_template = ChatPromptTemplate.from_template(
            "El siguiente es un chat entre un humano y un asistente de IA. El asistente es útil, amigable y experto. "
            "Presta especial atención a las fechas del documento, las cuales aparecen en diferentes formatos.\n"
            "en documentación.\n"
            "{chat_history}\nHuman: {input}\nAssistant:"
        )
        qa_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=False)

    if len(msgs.messages) == 0 or st.sidebar.button("Limpiar historial"):
        msgs.clear()
        msgs.add_ai_message("En qué puedo ayudarte?")

    avatars = {"human": "user", "ai": "🤖"}
    for msg in msgs.messages:
        st.chat_message(avatars[msg.type]).write(msg.content)

    if user_query := st.chat_input(placeholder="Preguntame lo que quieras"):
        st.chat_message("user").write(user_query)
        # count_documents_in_chroma_db()
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            if retriever:
                # TODO Solventar que se imprima el Input en la respuesta al adjuntar un documento
                retrieval_handler = PrintRetrievalHandler(st.container())
                qa_chain.run({"question": user_query, "chat_history": memory.load_memory_variables({})["chat_history"]},
                             callbacks=[stream_handler, retrieval_handler])
            else:
                response = qa_chain.run(
                    {"input": user_query, "chat_history": memory.load_memory_variables({})["chat_history"]},
                    callbacks=[stream_handler])
