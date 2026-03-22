import streamlit as st
from langchain_core.prompts import ChatPromptTemplate


class ResumeAnalyzerNode:
    def __init__(self, llm):
        self.llm = llm
        self.state = {}

    def extract_resume(self, state: dict) -> dict:
        """
        Node 1: Reads already-extracted resume text from state
        """
        try:
            resume_text = state["messages"][0].content

            if not resume_text:
                raise ValueError("Resume text is empty")

            state["resume_text"] = resume_text
            self.state["resume_text"] = resume_text
            return state

        except Exception as e:
            raise ValueError(f"Error in extract_resume node: {e}")

    def analyze_resume(self, state: dict) -> dict:
        """
        Node 2: Analyzes the resume using LLM and generates feedback
        """
        try:
            resume_text = self.state.get("resume_text", "")

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", """You are an expert HR recruiter and resume analyst with 10+ years of experience.
                Analyze the given resume thoroughly and provide a detailed evaluation in the following format:

                ## 👤 Candidate Overview
                - Name, current role, years of experience (if found)

                ## ✅ Strengths
                - List what the candidate did well (skills, experience, achievements, formatting)

                ## ❌ Weaknesses
                - List what is missing or needs improvement

                ## 📊 Section-wise Score
                - Skills: X/20
                - Experience: X/30
                - Education: X/20
                - Achievements: X/15
                - Formatting & Clarity: X/15
                - Total Score: X/100

                ## 🎯 Verdict
                - Selected or Not Selected
                - One line reason for the verdict

                ## 💡 Improvement Tips
                - Give 3-5 specific, actionable suggestions to improve the resume

                Be honest, specific and constructive in your feedback.
                """),
                ("user", "Here is the resume to analyze:\n\n{resume_text}")
            ])

            response = self.llm.invoke(
                prompt_template.format(resume_text=resume_text)
            )

            state["analysis"] = response.content
            self.state["analysis"] = response.content
            return state

        except Exception as e:
            raise ValueError(f"Error in analyze_resume node: {e}")

    def generate_report(self, state: dict) -> dict:
        """
        Node 3: Extracts score and verdict from analysis and finalizes report
        """
        try:
            analysis = self.state.get("analysis", "")

            report_prompt = ChatPromptTemplate.from_messages([
                ("system", """Extract the following from the resume analysis and return in this exact format:
                SCORE: (just the number out of 100)
                VERDICT: (just Selected or Not Selected)
                """),
                ("user", "Analysis:\n\n{analysis}")
            ])

            response = self.llm.invoke(
                report_prompt.format(analysis=analysis)
            )

            lines = response.content.strip().split("\n")
            score = 0
            verdict = "Not Selected"

            for line in lines:
                if line.startswith("SCORE:"):
                    try:
                        score = int(line.replace("SCORE:", "").strip())
                    except:
                        score = 0
                elif line.startswith("VERDICT:"):
                    verdict = line.replace("VERDICT:", "").strip()

            self.state["score"] = score
            self.state["verdict"] = verdict
            state["score"] = score
            state["verdict"] = verdict

            return self.state

        except Exception as e:
            raise ValueError(f"Error in generate_report node: {e}")