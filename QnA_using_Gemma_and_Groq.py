import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import time

#load API keys
load_dotenv()
groq_api_key = os.getenv("Groq_API_key")
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

#setup streamlit
st.title("Gemma Model Document QnA")

#load Gemma model through Groq
llm=ChatGroq(groq_api_key=groq_api_key,model_name="gemma2-9b-it")
# print(llm)

#setup the prompt template
prompt=ChatPromptTemplate.from_template(
""" 
Answer the questions based on the provided context only,
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}
""")

def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader=PyPDFDirectoryLoader("./AI_papers") ## Data Ingestion
        st.session_state.docs=st.session_state.loader.load() ## Document loading
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

prompt1=st.text_input("What do you want to ask from the documents?")


if st.button("Create vector store"):
    vector_embedding()
    st.write("Vector store DB is ready")

if prompt1:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retriever_chain=create_retrieval_chain(retriever,document_chain)

    start=time.process_time()
    response=retriever_chain.invoke({'input':prompt1})
    st.write(response['answer'])

    #with a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")
