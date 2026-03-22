import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class GoogleGeminiLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            google_api_key = self.user_controls_input.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
            selected_model = self.user_controls_input.get("selected_google_model", "gemini-1.5-flash")

            if not google_api_key:
                st.error("Please enter your Google API Key")
                return None

            llm = ChatGoogleGenerativeAI(api_key=google_api_key, model=selected_model)

        except Exception as e:
            raise ValueError(f"Error occurred with Gemini LLM: {e}")

        return llm