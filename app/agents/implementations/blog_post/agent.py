from app.agents.core.base_agent import BaseAgent
from app.utils.types import EdgeType, NodeType, ToolType
from langgraph.graph import END, START
from langgraph.prebuilt import tools_condition

class BlogPostAgent(BaseAgent):
    """Agent specialized in searching and analyzing blog posts"""
    def __init__(self):
        super().__init__(
            tool_types=[ToolType.BLOG_SEARCH],
            edge_types=[EdgeType.GRADE_DOCUMENTS],
            node_types=[NodeType.AGENT, NodeType.GENERATE, NodeType.REWRITE]
        )
    
    def prepare(self):
        events = self.setup_events()
        retriever_tool, edges, nodes = events

        self.workflow.add_node("agent", nodes[NodeType.AGENT])
        self.workflow.add_node("retrieve", retriever_tool)
        self.workflow.add_node("rewrite", nodes[NodeType.REWRITE])
        self.workflow.add_node("generate", nodes[NodeType.GENERATE])
        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "retrieve", END: END}
        )
        self.workflow.add_conditional_edges(
            "retrieve",
            edges[EdgeType.GRADE_DOCUMENTS],
        )
        self.workflow.add_edge("generate", END)
        self.workflow.add_edge("rewrite", "agent")

        return self.workflow

    def process(self):
        message = self.execute(self.prepare(), {
            "query": "How Harrison Chase defines an agent?"
        })
        return message