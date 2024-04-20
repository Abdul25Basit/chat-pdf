import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyMuPDFLoader


import streamlit as st

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

def load_doc(pdf_doc):

  loader = PyMuPDFLoader(pdf_doc)
  documents = loader.load()
  embedding = HuggingFaceEmbeddings()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  text = text_splitter.split_documents(documents)
  db = Chroma.from_documents(text, embedding)
  llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-1-pythia-12b", model_kwargs={"temperature": 1.0, "max_length": 256})
  global chain
  chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff",retriever=db.as_retriever())
  return 'Document has successfully been loaded'

def answer_query(query):
  question = query
  return chain.run(question)

st.title("ChatPDF")
st.write("Upload a PDF File and then click on Load PDF File")
st.write("Once the document has been loaded you can begin chatting with the PDF =)")

uploaded_pdf = st.file_uploader("Load a pdf", type=['.pdf','.docx'])

if uploaded_pdf is not None:
  status = st.text_input("Status", "", key="status")
  status.value = load_doc(uploaded_pdf)

  query = st.text_input("type in your question")
  output = st.text_area("output", "", height=100)

  if st.button("submit"):
    output.value = answer_query(query)
