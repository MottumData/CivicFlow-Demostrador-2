import os
import tempfile
import logging

import chromadb
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma

from conf.project_path import CHROMA_DB_PATH
from conf.logging_config import get_logger
from src.utils import get_openai_api_key

logger = get_logger(__name__)


# TODO Hacer un chat y no solo mensaje-respuesta
# TODO Eliminar informacion innecesaria del chat:
#  - Vector store
#  - Procesar informacion con éxito (retrieval)
# TODO Hacer que tenga un mejor referencia del contexto
# TODO Utilizar los runnables
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Procesando información del contexto**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        self.status.write(f"**Question:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata.get("source", "Desconocido"))
            self.status.write(f"**Document {idx} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")

        #
        #
        # @st.cache_resource(ttl="8h")
        # def configure_retriever(uploaded_files):
        #     docs = []
        #     temp_dir = tempfile.TemporaryDirectory()
        #     for file in uploaded_files:
        #         temp_filepath = os.path.join(temp_dir.name, file.name)
        #         with open(temp_filepath, "wb") as f:
        #             f.write(file.getvalue())
        #         loader = PyPDFLoader(temp_filepath)
        #         docs.extend(loader.load())
        #
        #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=2,
        #                                                    separators=["\n\n", "\n", ".", " ", ""])
        #     splits = text_splitter.split_documents(docs)
        #
        #     embeddings_model_name = "sentence-transformers/all-MiniLM-L12-v2"
        #
        #     embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        #
        #     # Se crea la base de datos de vectores en memoria
        #     # vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
        #     #
        #
        #     # Se crea el directorio para almacenar la base de datos de Chroma
        #     vectordb = Chroma.from_documents(splits, embeddings, collection_name='documentos_adjuntos',
        #                                      persist_directory=CHROMA_DB_PATH)
        #     # vectordb.persist()
        #     retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 5})
        #
        #     return retriever
        #
        #
        # @st.cache_resource
        # def get_retriever(openai_api_key=None):
        #     embeddings_model_name = "sentence-transformers/paraphrase-xlm-r-multilingual-v1"
        #     embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        #     return ensemble_retriever_from_docs(docs, embeddings=embeddings)
        #
        #
        # def get_chain(openai_api_key=None, huggingfacehub_api_token=None):
        #     ensemble_retriever = get_retriever(openai_api_key=openai_api_key)
        #     chain = create_full_chain(ensemble_retriever,
        #                               openai_api_key=openai_api_key,
        #                               chat_memory=StreamlitChatMessageHistory(key="langchain_messages"))
        #     return chain
        #
        #
        # def get_openai_api_key():
        #     return os.getenv("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else st.sidebar.text_input("OpenAI API Key",
        #                                                                                                     type="password",
        #                                                                                                     key='openai_api_key_input')
        #
        #
        # def show_chats_page():
        #     st.write("Chats")
        #     st.sidebar.write("Conversaciones")
        #     openai_api_key = get_openai_api_key()
        #     if not openai_api_key:
        #         st.info("Please add your OpenAI API key to continue.")
        #         st.stop()
        #
        #     model_name = st.sidebar.selectbox("Selecciona un modelo", ["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
        #                                       index=3)
        #     st.write("Modelo seleccionado:", model_name)
        #
        #     uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=True)
        #
        #     retriever = configure_retriever(uploaded_files) if uploaded_files else None
        #
        #     msgs = StreamlitChatMessageHistory()
        #
        #     memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)
        #
        #     llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True)
        #
        #     if retriever:
        #         # Ajustamos la plantilla para incluir el contexto de documentos
        #         prompt_template = ChatPromptTemplate.from_template(
        #             "Eres un asistente IA experto en documentación y análisis.\n"
        #             "Historial de conversación:\n{chat_history}\n"
        #             "Información relevante:\n{context}\n"
        #             "Sin repetir la pregunta, responde de la manera más concisa posible a la siguiente consulta basada en la información relevante:\n"
        #             "{question}"
        #         )
        #         # TODO Cambiar la función ConversationalRetrievalChain por create_retrieval_chain
        #         qa_chain = ConversationalRetrievalChain.from_llm(
        #             llm=llm,
        #             retriever=retriever,
        #             memory=memory,
        #             verbose=False,
        #             combine_docs_chain_kwargs={
        #                 "prompt": prompt_template,
        #                 "document_variable_name": "context"  # Aseguramos que la variable se llame 'context'
        #             }
        #         )
        #     else:
        #         # Prompt en caso de que no haya retriever
        #         prompt_template = ChatPromptTemplate.from_template(
        #             "El siguiente es un chat entre un humano y un asistente de IA. El asistente es útil, amigable y experto en documentación.\n"
        #             "{chat_history}\nHuman: {input}\nAssistant:"
        #         )
        #         qa_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=False)
        #
        #     if len(msgs.messages) == 0 or st.sidebar.button("Limpiar historial"):
        #         msgs.clear()
        #         msgs.add_ai_message("Hola! En qué puedo ayudarte?")
        #
        #     avatars = {"human": "user", "ai": "assistant"}
        #     for msg in msgs.messages:
        #         st.chat_message(avatars[msg.type]).write(msg.content)
        #
        #     if user_query := st.chat_input(placeholder="Preguntame lo que quieras"):
        #         st.chat_message("user").write(user_query)
        #
        #         with st.chat_message("assistant"):
        #             stream_handler = StreamHandler(st.empty())
        #             if retriever:
        #                 # TODO Solventar que se imprima el Input en la respuesta al adjuntar un documento
        #                 retrieval_handler = PrintRetrievalHandler(st.container())
        #                 qa_chain.run({"input": user_query, "chat_history": memory.load_memory_variables({})["chat_history"]},
        #                              callbacks=[stream_handler, retrieval_handler])
        #             else:
        #                 response = qa_chain.run(
        #                     {"input": user_query, "chat_history": memory.load_memory_variables({})["chat_history"]},
        #                     callbacks=[stream_handler])


def create_qa_chain(retriever, model_name, output_container):
    """Crea la cadena de preguntas y respuestas con historial de conversación."""
    # Define el prompt del sistema
    system_prompt = (
        "Usa el contexto recuperado para responder la pregunta. Si no sabes la respuesta, indica que no la sabes."
        "\n\nContexto:\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    openai_api_key = get_openai_api_key()
    # Configura el modelo de lenguaje
    llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key, temperature=0, streaming=True)

    # Handler para la salida de tokens en tiempo real
    stream_handler = StreamHandler(output_container)

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain


def initialize_chat_history():
    """Inicializa el historial de conversación en la sesión de Streamlit."""
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []


def user_interface(rag_chain, output_container):
    # if user_input := st.text_input("Preguntame lo que quieras"):
    user_input = st.chat_input("Preguntame lo que quieras")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        # Handle the response
        response = rag_chain.invoke({
            "input": user_input,
            "chat_history": st.session_state['chat_history']
        },
            {'callback': StreamHandler(output_container)}
        )

        answer = response.get("answer", "")

        # Display AI response in chat format
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Update the chat history
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        st.session_state['chat_history'].append({"role": "assistant", "content": answer})


def load_retriever(output_container, uploaded_files=None):
    persist_directory = CHROMA_DB_PATH
    embeddings_model_name = "sentence-transformers/paraphrase-xlm-r-multilingual-v1"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, show_progress=True)
    if os.path.exists(persist_directory) and not uploaded_files:
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        st.info("Base de datos de vectores previamente cargada.")
    else:
        retrival_handler = PrintRetrievalHandler(output_container)
        docs = []
        temp_dir = tempfile.TemporaryDirectory()
        for file in uploaded_files:
            temp_filepath = os.path.join(temp_dir.name, file.name)
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())
            loader = PyPDFLoader(temp_filepath)
            docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=150,
                                                       separators=["\n\n", "\n", ".", " ", ""])
        splits = text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        # vector_store.persist()
        st.info("Vectorstore creado y almacenado de forma persistente.")

    retriever = vector_store.as_retriever()
    return retriever


def show_chats_page():
    st.write("Chats")
    initialize_chat_history()

    st.sidebar.write("Conversaciones")
    openai_api_key = get_openai_api_key()

    model_name = st.sidebar.selectbox("Selecciona un modelo", ["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
                                      index=3)
    st.write("Modelo seleccionado:", model_name)

    # uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=True)
    output_container = st.empty()

    uploaded_files = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=True)

    retriever = load_retriever(output_container, uploaded_files) if uploaded_files else load_retriever(output_container)
    rag_chain = create_qa_chain(retriever=retriever, model_name=model_name, output_container=output_container)

    user_interface(rag_chain, output_container)
