import streamlit as st
import os
from src.langchainagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title="🤖 " + self.config.get_page_title(),
            page_icon="📄",
            layout="wide"
        )

        st.title("🤖 " + self.config.get_page_title())
        st.markdown("Upload your resume and get instant AI-powered feedback!")

        # Reset session state defaults
        if "analyze_clicked" not in st.session_state:
            st.session_state.analyze_clicked = False
        if "uploaded_resume" not in st.session_state:
            st.session_state.uploaded_resume = None

        with st.sidebar:
            st.header("⚙️ Configuration")

            # LLM Selection
            llm_options = self.config.get_llm_options()
            self.user_controls["selected_llm"] = st.selectbox(
                "Select LLM", llm_options
            )

            # Groq config
            if self.user_controls["selected_llm"] == "Groq":
                groq_model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Groq Model", groq_model_options
                )
                self.user_controls["GROQ_API_KEY"] = st.text_input(
                    "Groq API Key (optional)",
                    type="password",
                    help="Leave empty to use key from .env file"
                )

            # Google Gemini config
            elif self.user_controls["selected_llm"] == "Google Gemini":
                gemini_model_options = self.config.get_google_gemini_model_options()
                self.user_controls["selected_google_model"] = st.selectbox(
                    "Select Gemini Model", gemini_model_options
                )
                self.user_controls["GOOGLE_API_KEY"] = st.text_input(
                    "Google API Key (optional)",
                    type="password",
                    help="Leave empty to use key from .env file"
                )

            # Usecase selection
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox(
                "Select Usecase", usecase_options
            )

            st.divider()
            st.markdown("### 📄 Upload Resume")

            # File uploader
            uploaded_file = st.file_uploader(
                "Upload your Resume",
                type=["pdf", "docx"],
                help="Supported formats: PDF, DOCX"
            )

            if uploaded_file:
                st.session_state.uploaded_resume = uploaded_file
                st.success(f"✅ {uploaded_file.name} uploaded!")

            # Analyze button
            if st.button("🔍 Analyze Resume", use_container_width=True):
                if not uploaded_file:
                    st.warning("⚠️ Please upload a resume first!")
                else:
                    st.session_state.analyze_clicked = True

        return self.user_controls