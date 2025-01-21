import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import streamlit as st
from db_functions import create_users_db, create_messages_db
from htmlTemplates import css, bot_template, user_template

# Load environment variables
load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)

def update_vectorstore(text_chunks, vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    if os.path.exists(vectorstore_path):
        vectorstore = FAISS.load_local(vectorstore_path, embeddings)
    else:
        vectorstore = FAISS.from_texts(text_chunks, embeddings)
    vectorstore.save_local(vectorstore_path)
    return vectorstore

def create_retrieval_chain(vectorstore_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vectorstore_path, embeddings)
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    )

def sidebar():
    with st.sidebar:
        st.header("Knowledge Base Upload")
        uploaded_files = st.file_uploader("Upload your documents (PDFs only):", type=["pdf"], accept_multiple_files=True)
        if uploaded_files and st.button("Process and Update"):
            raw_text = get_pdf_text(uploaded_files)
            text_chunks = get_text_chunks(raw_text)
            update_vectorstore(text_chunks)
            st.success("Knowledge base updated successfully!")

def main():
    st.set_page_config(page_title="AI Knowledge Base", page_icon="🤖")
    st.write(css, unsafe_allow_html=True)
    sidebar()
    st.title("AI Knowledge Base")
    st.caption("Upload documents to expand the AI's knowledge.")
    st.write("Start by uploading documents through the sidebar to enable retrieval from the enhanced knowledge base.")

if __name__ == '__main__':
    main()