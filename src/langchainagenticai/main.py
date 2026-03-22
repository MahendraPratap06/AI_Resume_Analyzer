import streamlit as st
from src.langchainagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langchainagenticai.LLMS.groqllm import GroqLLM
from src.langchainagenticai.LLMS.googlegeminiollm import GoogleGeminiLLM
from src.langchainagenticai.graph.graph_builder import GraphBuilder
from src.langchainagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langchain_agenticai_app():
    """
    Main orchestrator function that:
    1. Loads the UI
    2. Gets user inputs
    3. Initializes the LLM
    4. Builds the graph
    5. Displays the result
    """

    # Step 1: Load UI and get user controls
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from UI.")
        return

    # Step 2: Get uploaded resume file
    uploaded_file = st.session_state.get("uploaded_resume", None)

    if st.session_state.get("analyze_clicked", False) and uploaded_file:
        try:
            # Step 3: Initialize LLM based on user selection
            selected_llm = user_input.get("selected_llm")

            if selected_llm == "Groq":
                obj_llm = GroqLLM(user_controls_input=user_input)
            elif selected_llm == "Google Gemini":
                obj_llm = GoogleGeminiLLM(user_controls_input=user_input)
            else:
                st.error("Please select a valid LLM.")
                return

            model = obj_llm.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            # Step 4: Get selected usecase
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No usecase selected.")
                return

            # Step 5: Build and run the graph
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(
                    usecase, graph, uploaded_file
                ).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return

        except Exception as e:
            st.error(f"Error: Application failed - {e}")
            return
