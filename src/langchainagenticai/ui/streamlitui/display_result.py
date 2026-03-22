import streamlit as st
from langchain_core.messages import HumanMessage
from src.langchainagenticai.utils.pdf_extractor import ResumeExtractor


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, uploaded_file):
        self.usecase = usecase
        self.graph = graph
        self.uploaded_file = uploaded_file

    def display_result_on_ui(self):
        if self.usecase == "Resume Analyzer":
            self._display_resume_analysis()

    def _display_resume_analysis(self):
        with st.spinner("🔍 Analyzing your resume... Please wait!"):
            try:
                # Extract text FIRST, then pass string to graph
                extractor = ResumeExtractor(self.uploaded_file)
                resume_text = extractor.extract_text()

                if not resume_text:
                    st.error("Could not extract text from resume.")
                    return

                result = self.graph.invoke({
                    "messages": [HumanMessage(content=resume_text)],
                })

                analysis = result.get("analysis", "")
                score = result.get("score", 0)
                verdict = result.get("verdict", "Not Selected")

                st.divider()
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(label="📊 Resume Score", value=f"{score}/100")

                with col2:
                    if verdict == "Selected":
                        st.success(f"🎯 Verdict: {verdict}")
                    else:
                        st.error(f"🎯 Verdict: {verdict}")

                st.divider()
                st.markdown("## 📋 Detailed Analysis")
                st.markdown(analysis)

            except Exception as e:
                st.error(f"Error displaying result: {e}")