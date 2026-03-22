import fitz
import docx2txt
import streamlit as st


class ResumeExtractor:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def extract_text(self):
        try:
            file_name = self.uploaded_file.name

            if file_name.endswith(".pdf"):
                return self._extract_from_pdf()

            elif file_name.endswith(".docx"):
                return self._extract_from_docx()

            else:
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
                return None

        except Exception as e:
            raise ValueError(f"Error extracting text from resume: {e}")

    def _extract_from_pdf(self):
        try:
            pdf_bytes = self.uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            if not text.strip():
                st.error("PDF appears to be empty or scanned. Please upload a text-based PDF.")
                return None
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")

    def _extract_from_docx(self):
        try:
            text = docx2txt.process(self.uploaded_file)
            if not text.strip():
                st.error("DOCX file appears to be empty.")
                return None
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {e}")
