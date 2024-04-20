import streamlit as st
import os

# For PDF loading (choose either PyMuPDFLoader or PyPDF2)
# Option 1: PyMuPDFLoader (if compatible with your environment)
# from langchain_community.document_loaders import PyMuPDFLoader

# Option 2: PyPDF2 (alternative PDF loading library)
import PyPDF2

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyMuPDFLoader  # Optional, if using PyMuPDFLoader

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"


def load_doc(pdf_doc):
  """Loads the text content from the uploaded PDF file."""

  # Option 1: Using PyMuPDFLoader (if compatible)
  # try:
  #   loader = PyMuPDFLoader(pdf_doc)
  #   documents = loader.load()
  #   # Rest of the text processing logic using documents...
  # except Exception as e:
  #   st.error(f"Error loading PDF: {e}")
  #   return None

  # Option 2: Using PyPDF2
  try:
    pdf_reader = PyPDF2.PdfReader(pdf_doc)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text
  except Exception as e:
    st.error(f"Error loading PDF: {e}")
    return None


def answer_query(query):
  question = query
  return chain.run(question)

st.title("ChatPDF")
st.write("Upload a PDF File and then click on Load PDF File")
st.write("Once the document has been loaded you can begin chatting with the PDF =)")

uploaded_pdf = st.file_uploader("Load a pdf", type=['.pdf', '.docx'])

if uploaded_pdf is not None:
  if uploaded_pdf.type not in ['.pdf', '.docx']:
    st.error("Please upload a valid PDF file.")
    continue
  
  status = st.text_input("Status", "", key="status")
  text = load_doc(uploaded_pdf)  # Call load_doc function
  if text is not None:
    status.value = "Document loaded successfully!"
  else:
    status.value = "Error loading document."

  query = st.text_input("type in your question")
  output = st.text_area("output", "", height=100)

  if st.button("submit"):
    if text is not None:  # Check if text was loaded successfully
      output.value = answer_query(query)
    else:
      st.error("Please load a valid PDF document before asking questions.")

