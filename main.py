import streamlit as st
import PyPDF2

def load_doc(pdf_doc):
    """Loads the text content from the uploaded PDF file using PyPDF2."""
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

st.title("ChatPDF")
st.write("Upload a PDF File and then click on Load PDF File")
st.write("Once the document has been loaded you can begin chatting with the PDF =)")

uploaded_pdf = st.file_uploader("Load a pdf", type=['.pdf', '.docx'])
if uploaded_pdf is not None:
    print(f"Uploaded file type: {uploaded_pdf.type}")  # Debugging statement
    if uploaded_pdf.type not in ['.pdf', '.docx']:
        st.error("Please upload a valid PDF file.")
    else:
        status = st.text_input("Status", "", key="status")
        text = load_doc(uploaded_pdf)
        print(f"Text extracted from PDF: {text}")  # Debugging statement
        if text is not None:
            status.value = "Document loaded successfully!"
        else:
            status.value = "Error loading document."

        query = st.text_input("Type in your question")
        output = st.text_area("Output", "", height=100)

        if st.button("Submit"):
            if text is not None:
                output.value = answer_query(query, text)
            else:
                st.error("Please load a valid PDF document before asking questions.")

