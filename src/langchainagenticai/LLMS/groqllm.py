import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY", "")
            selected_model = self.user_controls_input.get("selected_groq_model", "llama3-8b-8192")

            if not groq_api_key:
                st.error("Please enter your GROQ API Key")
                return None

            llm = ChatGroq(api_key=groq_api_key, model=selected_model)

        except Exception as e:
            raise ValueError(f"Error occurred with Groq LLM: {e}")

        return llm