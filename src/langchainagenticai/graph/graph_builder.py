from langgraph.graph import StateGraph, START, END
from src.langchainagenticai.state.state import State
from src.langchainagenticai.nodes.resume_analyzer_node import ResumeAnalyzerNode


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def resume_analyzer_build_graph(self):
        """
        Builds the resume analyzer graph with 3 nodes:
        extract_resume → analyze_resume → generate_report
        """
        resume_node = ResumeAnalyzerNode(self.llm)

        # Add nodes
        self.graph_builder.add_node("extract_resume", resume_node.extract_resume)
        self.graph_builder.add_node("analyze_resume", resume_node.analyze_resume)
        self.graph_builder.add_node("generate_report", resume_node.generate_report)

        # Add edges
        self.graph_builder.set_entry_point("extract_resume")
        self.graph_builder.add_edge("extract_resume", "analyze_resume")
        self.graph_builder.add_edge("analyze_resume", "generate_report")
        self.graph_builder.add_edge("generate_report", END)

    def setup_graph(self, usecase: str):
        """
        Sets up and compiles the graph based on selected usecase
        """
        if usecase == "Resume Analyzer":
            self.resume_analyzer_build_graph()

        return self.graph_builder.compile()
